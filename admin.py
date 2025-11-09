# admin.py
"""
Admin Panel - Dashboard, Destinations, Categories, Routes, Users Management
Converted from admin/*.php
"""

from fastapi import APIRouter, Request, Depends, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import Optional, List
from pathlib import Path
import shutil
from datetime import datetime

from config.database import (
    get_db, Destination, Category, Review, Route, User, 
    DestinationImage, WebsiteFeedback, UPLOAD_PATH, UPLOAD_URL
)
from auth import require_admin, get_password_hash

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="templates")


# Helper function to save uploaded file
async def save_upload_file(upload_file: UploadFile, subfolder: str = "destinations") -> str:
    """Save uploaded file and return the path"""
    
    # Create unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_str = upload_file.filename if upload_file.filename else "unknown"
    extension = Path(filename_str).suffix
    filename = f"{timestamp}_{filename_str}"
    
    # Full path
    upload_dir = UPLOAD_PATH / subfolder
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / filename
    
    # Save file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    # Return relative path
    return f"{subfolder}/{filename}"


@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Admin Dashboard - Overview Statistics"""
    
    # Statistics
    total_destinations = db.query(func.count(Destination.id)).scalar() or 0
    active_destinations = db.query(func.count(Destination.id)).filter(Destination.is_active.is_(True)).scalar() or 0
    total_categories = db.query(func.count(Category.id)).scalar() or 0
    total_routes = db.query(func.count(Route.id)).scalar() or 0
    unread_feedback = db.query(func.count(WebsiteFeedback.id)).filter(WebsiteFeedback.is_read.is_(False)).scalar() or 0
    
    # Recent destinations
    recent_destinations = db.query(
        Destination,
        Category.name.label('category_name')
    ).outerjoin(
        Category, Destination.category_id == Category.id
    ).order_by(Destination.created_at.desc()).limit(5).all()
    
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "total_destinations": total_destinations,
        "active_destinations": active_destinations,
        "total_categories": total_categories,
        "total_routes": total_routes,
        "unread_feedback": unread_feedback,
        "recent_destinations": recent_destinations
    })


@router.get("/destinations", response_class=HTMLResponse)
async def admin_destinations(
    request: Request,
    search: str = "",
    category: int = 0,
    success: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Manage Destinations - List View"""
    
    # Build query
    query = db.query(
        Destination,
        Category.name.label('category_name')
    ).outerjoin(
        Category, Destination.category_id == Category.id
    )
    
    # Apply filters
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Destination.name.like(search_term)) | 
            (Destination.description.like(search_term))
        )
    
    if category > 0:
        query = query.filter(Destination.category_id == category)
    
    destinations = query.order_by(Destination.created_at.desc()).all()
    
    # Get categories for filter
    categories = db.query(Category).order_by(Category.name).all()
    
    # Get unread feedback count
    unread_feedback = db.query(func.count(WebsiteFeedback.id)).filter(WebsiteFeedback.is_read.is_(False)).scalar() or 0
    
    return templates.TemplateResponse("admin/destinations.html", {
        "request": request,
        "current_user": current_user,
        "destinations": destinations,
        "categories": categories,
        "search": search,
        "category_filter": category,
        "success": success,
        "unread_feedback": unread_feedback,
        "UPLOAD_URL": UPLOAD_URL
    })


@router.get("/destinations/add", response_class=HTMLResponse)
async def add_destination_form(
    request: Request,
    id: Optional[int] = None,
    success: Optional[str] = None,
    error: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Add/Edit Destination Form"""
    
    # Check if editing
    destination = None
    existing_photos: List[DestinationImage] = []
    
    if id:
        destination = db.query(Destination).filter(Destination.id == id).first()
        if not destination:
            return RedirectResponse(url="/admin/destinations", status_code=303)
        
        # Get existing photos
        existing_photos = db.query(DestinationImage).filter(
            DestinationImage.destination_id == id
        ).order_by(DestinationImage.id).all()
    
    # Get categories
    categories = db.query(Category).order_by(Category.name).all()
    
    # Get unread feedback count
    unread_feedback = db.query(func.count(WebsiteFeedback.id)).filter(WebsiteFeedback.is_read.is_(False)).scalar() or 0
    
    return templates.TemplateResponse("admin/add_destination.html", {
        "request": request,
        "current_user": current_user,
        "destination": destination,
        "categories": categories,
        "existing_photos": existing_photos,
        "edit_mode": id is not None,
        "success": success,
        "error": error,
        "unread_feedback": unread_feedback,
        "UPLOAD_URL": UPLOAD_URL
    })


@router.post("/destinations/save")
async def save_destination(
    request: Request,
    id: Optional[int] = Form(None),
    name: str = Form(...),
    category_id: int = Form(...),
    description: str = Form(""),
    address: str = Form(""),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    contact_number: str = Form(""),
    email: str = Form(""),
    website: str = Form(""),
    opening_hours: str = Form(""),
    entry_fee: str = Form(""),
    rating: float = Form(0.0),
    is_active: bool = Form(False),
    image: Optional[UploadFile] = File(None),
    additional_photos: Optional[List[UploadFile]] = File(None),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Save (Create/Update) Destination"""
    
    try:
        # Handle main image upload
        image_path: Optional[str] = None
        if image and image.filename:
            image_path = await save_upload_file(image, "destinations")
        
        if id:
            # Update existing
            destination = db.query(Destination).filter(Destination.id == id).first()
            if not destination:
                raise HTTPException(status_code=404, detail="Destination not found")
            
            # Update fields
            destination.name = name
            destination.category_id = category_id
            destination.description = description
            destination.address = address
            destination.latitude = latitude
            destination.longitude = longitude
            destination.contact_number = contact_number
            destination.email = email
            destination.website = website
            destination.opening_hours = opening_hours
            destination.entry_fee = entry_fee
            destination.rating = rating
            destination.is_active = is_active
            
            if image_path:
                destination.image_path = image_path
            
        else:
            # Create new
            destination = Destination(
                name=name,
                category_id=category_id,
                description=description,
                address=address,
                latitude=latitude,
                longitude=longitude,
                contact_number=contact_number,
                email=email,
                website=website,
                opening_hours=opening_hours,
                entry_fee=entry_fee,
                rating=rating,
                image_path=image_path,
                is_active=is_active
            )
            db.add(destination)
        
        db.commit()
        db.refresh(destination)
        
        # Handle additional photos
        if additional_photos and len(additional_photos) > 0 and additional_photos[0].filename:
            for photo in additional_photos:
                if photo.filename:
                    photo_path = await save_upload_file(photo, "destinations")
                    dest_image = DestinationImage(
                        destination_id=destination.id,
                        image_path=photo_path,
                        caption=""
                    )
                    db.add(dest_image)
            db.commit()
        
        return RedirectResponse(
            url=f"/admin/destinations?success={'updated' if id else 'created'}",
            status_code=303
        )
    
    except Exception as e:
        return RedirectResponse(
            url=f"/admin/destinations/add?error={str(e)}",
            status_code=303
        )


@router.get("/destinations/delete/{destination_id}")
async def delete_destination(
    destination_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete Destination"""
    
    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    if destination:
        db.delete(destination)
        db.commit()
    
    return RedirectResponse(url="/admin/destinations?success=deleted", status_code=303)


@router.get("/destinations/toggle/{destination_id}")
async def toggle_destination(
    destination_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Toggle Destination Active Status"""
    
    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    if destination:
        # Use .is_() for boolean comparison with SQLAlchemy
        current_status = db.query(Destination.is_active).filter(Destination.id == destination_id).scalar()
        destination.is_active = not current_status
        db.commit()
    
    return RedirectResponse(url="/admin/destinations?success=toggled", status_code=303)


@router.get("/categories", response_class=HTMLResponse)
async def admin_categories(
    request: Request,
    success: Optional[str] = None,
    error: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Manage Categories"""
    
    # Get categories with destination count
    categories = db.query(
        Category,
        func.count(Destination.id).label('destination_count')
    ).outerjoin(
        Destination, Category.id == Destination.category_id
    ).group_by(Category.id).order_by(Category.name).all()
    
    # Icon options
    icon_options = {
        'fa-camera': 'Camera',
        'fa-utensils': 'Restaurant',
        'fa-bed': 'Hotel',
        'fa-bus': 'Transport',
        'fa-landmark': 'Landmark',
        'fa-tree': 'Nature',
        'fa-shopping-bag': 'Shopping',
        'fa-film': 'Entertainment',
        'fa-church': 'Church',
        'fa-building': 'Building',
        'fa-monument': 'Monument',
        'fa-water': 'Beach',
        'fa-mountain': 'Mountain',
        'fa-coffee': 'Cafe',
        'fa-heart': 'Favorite'
    }
    
    # Get unread feedback count
    unread_feedback = db.query(func.count(WebsiteFeedback.id)).filter(WebsiteFeedback.is_read.is_(False)).scalar() or 0
    
    return templates.TemplateResponse("admin/categories.html", {
        "request": request,
        "current_user": current_user,
        "categories": categories,
        "icon_options": icon_options,
        "success": success,
        "error": error,
        "unread_feedback": unread_feedback
    })


@router.post("/categories/save")
async def save_category(
    request: Request,
    edit_id: Optional[int] = Form(None),
    name: str = Form(...),
    icon: str = Form(...),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Save Category"""
    
    if edit_id:
        # Update
        category = db.query(Category).filter(Category.id == edit_id).first()
        if category:
            category.name = name
            category.icon = icon
    else:
        # Create
        category = Category(name=name, icon=icon)
        db.add(category)
    
    db.commit()
    return RedirectResponse(url="/admin/categories?success=saved", status_code=303)


@router.get("/categories/delete/{category_id}")
async def delete_category(
    category_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete Category"""
    
    # Check if category has destinations
    count = db.query(func.count(Destination.id)).filter(Destination.category_id == category_id).scalar() or 0
    
    if count == 0:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            db.delete(category)
            db.commit()
            return RedirectResponse(url="/admin/categories?success=deleted", status_code=303)
    
    return RedirectResponse(url="/admin/categories?error=has_destinations", status_code=303)


@router.get("/users", response_class=HTMLResponse)
async def admin_users(
    request: Request,
    success: Optional[str] = None,
    error: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Manage Users"""
    
    users = db.query(User).order_by(User.created_at.desc()).all()
    
    # Get unread feedback count
    unread_feedback = db.query(func.count(WebsiteFeedback.id)).filter(WebsiteFeedback.is_read.is_(False)).scalar() or 0
    
    return templates.TemplateResponse("admin/users.html", {
        "request": request,
        "current_user": current_user,
        "users": users,
        "success": success,
        "error": error,
        "unread_feedback": unread_feedback
    })


@router.get("/users/toggle/{user_id}")
async def toggle_user_role(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Toggle User Role"""
    
    if user_id == current_user.id:
        return RedirectResponse(url="/admin/users?error=cannot_modify_self", status_code=303)
    
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.role = 'user' if user.role == 'admin' else 'admin'  # type: ignore
        db.commit()
    
    return RedirectResponse(url="/admin/users?success=role_updated", status_code=303)


@router.get("/users/delete/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete User"""
    
    if user_id == current_user.id:
        return RedirectResponse(url="/admin/users?error=cannot_delete_self", status_code=303)
    
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    
    return RedirectResponse(url="/admin/users?success=deleted", status_code=303)