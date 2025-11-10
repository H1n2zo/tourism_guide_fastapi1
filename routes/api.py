# routes/api.py
"""
Additional API Endpoints for Tourism Guide System
Provides REST API for mobile apps or third-party integrations
FIXED: All type checking errors resolved
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator

from config.database import (
    get_db, Destination, Category, Review, Route, 
    DestinationImage, WebsiteFeedback, User, UPLOAD_URL
)
from routes.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["api"])


# Pydantic models for request validation
class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    category: str = Field(..., description="Feedback category")
    feedback: str = Field(..., min_length=10, description="Feedback text")
    user_name: Optional[str] = None
    email: Optional[str] = None

    @validator('category')
    def validate_category(cls, v):
        valid_categories = ['usability', 'features', 'content', 'design', 'general']
        if v not in valid_categories:
            raise ValueError(f'Category must be one of: {", ".join(valid_categories)}')
        return v


# Helper function to safely convert to float
def safe_float(value: Union[float, None]) -> Optional[float]:
    """Safely convert value to float, returning None if value is None"""
    if value is None:
        return None
    return float(value)


# ==================== DESTINATIONS API ====================

@router.get("/destinations/{destination_id}")
async def get_destination_detail(
    destination_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific destination"""
    
    try:
        # Get destination with category
        dest_query = db.query(
            Destination,
            Category.name.label('category_name'),
            Category.icon.label('icon')
        ).outerjoin(
            Category, Destination.category_id == Category.id
        ).filter(
            Destination.id == destination_id
        ).first()
        
        if not dest_query:
            raise HTTPException(status_code=404, detail="Destination not found")
        
        dest, category_name, icon = dest_query
        
        # Get images
        images = db.query(DestinationImage).filter(
            DestinationImage.destination_id == destination_id
        ).all()
        
        # Get reviews
        reviews = db.query(Review).filter(
            Review.destination_id == destination_id,
            Review.is_approved.is_(True)
        ).order_by(Review.created_at.desc()).all()
        
        # Calculate rating stats
        rating_stats = db.query(
            func.count(Review.id).label('count'),
            func.avg(Review.rating).label('avg_rating')
        ).filter(
            Review.destination_id == destination_id,
            Review.is_approved.is_(True)
        ).first()
        
        return {
            "id": dest.id,
            "name": dest.name,
            "category_name": category_name,
            "icon": icon,
            "description": dest.description,
            "address": dest.address,
            "latitude": safe_float(dest.latitude),
            "longitude": safe_float(dest.longitude),
            "contact_number": dest.contact_number,
            "email": dest.email,
            "website": dest.website,
            "opening_hours": dest.opening_hours,
            "entry_fee": dest.entry_fee,
            "rating": safe_float(dest.rating) or 0.0,
            "is_active": dest.is_active,
            "image_path": f"{UPLOAD_URL}{dest.image_path}" if dest.image_path else None,
            "images": [
                {
                    "id": img.id,
                    "url": f"{UPLOAD_URL}{img.image_path}",
                    "caption": img.caption,
                    "is_primary": img.is_primary
                } for img in images
            ],
            "reviews": [
                {
                    "id": r.id,
                    "user_name": r.user_name,
                    "rating": r.rating,
                    "comment": r.comment,
                    "created_at": r.created_at.isoformat()
                } for r in reviews
            ],
            "review_count": rating_stats.count if rating_stats else 0,
            "average_rating": safe_float(rating_stats.avg_rating) if rating_stats and rating_stats.avg_rating else 0.0
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ==================== CATEGORIES API ====================

@router.get("/categories")
async def get_categories(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get all categories with destination count"""
    
    try:
        categories = db.query(
            Category,
            func.count(Destination.id).label('destination_count')
        ).outerjoin(
            Destination, Category.id == Destination.category_id
        ).group_by(Category.id).order_by(Category.name).all()
        
        return {
            "categories": [
                {
                    "id": cat.id,
                    "name": cat.name,
                    "icon": cat.icon,
                    "destination_count": count,
                    "created_at": cat.created_at.isoformat()
                } for cat, count in categories
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ==================== REVIEWS API ====================

@router.get("/destinations/{destination_id}/reviews")
async def get_destination_reviews(
    destination_id: int,
    request: Request,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get reviews for a destination with pagination"""
    
    try:
        # Check if destination exists
        dest = db.query(Destination).filter(Destination.id == destination_id).first()
        if not dest:
            raise HTTPException(status_code=404, detail="Destination not found")
        
        # Get reviews
        reviews = db.query(Review).filter(
            Review.destination_id == destination_id,
            Review.is_approved.is_(True)
        ).order_by(
            Review.created_at.desc()
        ).limit(limit).offset(offset).all()
        
        # Get total count
        total = db.query(func.count(Review.id)).filter(
            Review.destination_id == destination_id,
            Review.is_approved.is_(True)
        ).scalar() or 0
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "reviews": [
                {
                    "id": r.id,
                    "user_name": r.user_name,
                    "rating": r.rating,
                    "comment": r.comment,
                    "created_at": r.created_at.isoformat()
                } for r in reviews
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ==================== STATISTICS API ====================

@router.get("/statistics")
async def get_statistics(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get overall system statistics"""
    
    try:
        total_destinations = db.query(func.count(Destination.id)).scalar() or 0
        active_destinations = db.query(func.count(Destination.id)).filter(
            Destination.is_active.is_(True)
        ).scalar() or 0
        total_categories = db.query(func.count(Category.id)).scalar() or 0
        total_routes = db.query(func.count(Route.id)).scalar() or 0
        total_reviews = db.query(func.count(Review.id)).filter(
            Review.is_approved.is_(True)
        ).scalar() or 0
        total_users = db.query(func.count(User.id)).scalar() or 0
        
        # Top rated destinations
        top_rated = db.query(
            Destination.id,
            Destination.name,
            func.avg(Review.rating).label('avg_rating'),
            func.count(Review.id).label('review_count')
        ).join(
            Review, Destination.id == Review.destination_id
        ).filter(
            Review.is_approved.is_(True)
        ).group_by(
            Destination.id, Destination.name
        ).having(
            func.count(Review.id) >= 3
        ).order_by(
            func.avg(Review.rating).desc()
        ).limit(5).all()
        
        return {
            "total_destinations": total_destinations,
            "active_destinations": active_destinations,
            "total_categories": total_categories,
            "total_routes": total_routes,
            "total_reviews": total_reviews,
            "total_users": total_users,
            "top_rated_destinations": [
                {
                    "id": dest_id,
                    "name": name,
                    "average_rating": safe_float(avg_rating) or 0.0,
                    "review_count": review_count
                } for dest_id, name, avg_rating, review_count in top_rated
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ==================== SEARCH API ====================

@router.get("/search")
async def search_destinations(
    request: Request,
    q: str = Query(..., min_length=2, description="Search query"),
    category_id: Optional[int] = None,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search destinations by name or description"""
    
    try:
        search_term = f"%{q}%"
        
        query = db.query(
            Destination,
            Category.name.label('category_name'),
            func.count(Review.id).label('review_count'),
            func.avg(Review.rating).label('avg_rating')
        ).outerjoin(
            Category, Destination.category_id == Category.id
        ).outerjoin(
            Review, (Destination.id == Review.destination_id) & (Review.is_approved.is_(True))
        ).filter(
            Destination.is_active.is_(True)
        ).filter(
            (Destination.name.like(search_term)) | 
            (Destination.description.like(search_term)) |
            (Destination.address.like(search_term))
        )
        
        if category_id:
            query = query.filter(Destination.category_id == category_id)
        
        results = query.group_by(Destination.id).limit(limit).all()
        
        return {
            "query": q,
            "count": len(results),
            "results": [
                {
                    "id": dest.id,
                    "name": dest.name,
                    "category_name": cat_name,
                    "description": dest.description[:150] + "..." if dest.description and len(dest.description) > 150 else dest.description,
                    "latitude": safe_float(dest.latitude),
                    "longitude": safe_float(dest.longitude),
                    "image_path": f"{UPLOAD_URL}{dest.image_path}" if dest.image_path else None,
                    "review_count": review_count or 0,
                    "average_rating": safe_float(avg_rating) or 0.0
                } for dest, cat_name, review_count, avg_rating in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ==================== NEARBY API ====================

@router.get("/nearby")
async def get_nearby_destinations(
    request: Request,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(5.0, ge=0.1, le=50),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get destinations near a specific location
    Uses simple distance calculation (not accurate for large distances)
    """
    
    try:
        # Simple distance calculation (approximate)
        destinations = db.query(Destination).filter(
            Destination.is_active.is_(True),
            Destination.latitude.isnot(None),
            Destination.longitude.isnot(None)
        ).all()
        
        nearby = []
        for dest in destinations:
            # Safe conversion with null check
            dest_lat = safe_float(dest.latitude)
            dest_lng = safe_float(dest.longitude)
            
            if dest_lat is None or dest_lng is None:
                continue
            
            lat_diff = dest_lat - latitude
            lng_diff = dest_lng - longitude
            # Simple Euclidean distance (approximate)
            distance = ((lat_diff ** 2) + (lng_diff ** 2)) ** 0.5
            distance_km = distance * 111  # Rough conversion to km
            
            if distance_km <= radius_km:
                nearby.append({
                    "id": dest.id,
                    "name": dest.name,
                    "latitude": dest_lat,
                    "longitude": dest_lng,
                    "distance_km": round(distance_km, 2),
                    "image_path": f"{UPLOAD_URL}{dest.image_path}" if dest.image_path else None
                })
        
        # Sort by distance
        nearby.sort(key=lambda x: x["distance_km"])
        
        return {
            "center": {"latitude": latitude, "longitude": longitude},
            "radius_km": radius_km,
            "count": len(nearby[:limit]),
            "destinations": nearby[:limit]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ==================== FEEDBACK API ====================

@router.post("/feedback")
async def submit_feedback(
    request: Request,
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db)
):
    """Submit website feedback"""
    
    try:
        new_feedback = WebsiteFeedback(
            user_name=feedback_data.user_name,
            email=feedback_data.email,
            rating=feedback_data.rating,
            category=feedback_data.category,
            feedback=feedback_data.feedback,
            is_public=True,
            is_read=False
        )
        
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        
        return {
            "success": True,
            "message": "Thank you for your feedback!",
            "id": new_feedback.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")