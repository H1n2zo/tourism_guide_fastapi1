from fastapi import FastAPI, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from contextlib import asynccontextmanager
import uvicorn

from config.database import (
    get_db, Destination, Category, Review, Route, UPLOAD_URL, 
    create_tables, test_connection
)

# Import routers
from routes.auth import router as auth_router, get_current_user
from routes.destination import router as destination_router
from routes.admin import router as admin_router


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("🚀 Starting Tourism Guide System...")
    test_connection()
    create_tables()
    print("✅ Application ready!")
    yield
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Tourism Guide System",
    description="Explore amazing places in Ormoc City",
    version="2.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Add custom Jinja2 filters
def nl2br(value):
    if value:
        return value.replace('\n', '<br>')
    return value

templates.env.filters['nl2br'] = nl2br

# Include routers
app.include_router(auth_router)
app.include_router(destination_router)
app.include_router(admin_router)


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    category: Optional[int] = Query(0, alias="category"),
    search: Optional[str] = Query("", alias="search"),
    db: Session = Depends(get_db)
):
    """Homepage - Main landing page"""
    
    current_user = get_current_user(request, db)
    
    # Statistics
    total_destinations = db.query(func.count(Destination.id)).filter(Destination.is_active.is_(True)).scalar() or 0
    total_reviews = db.query(func.count(Review.id)).filter(Review.is_approved.is_(True)).scalar() or 0
    total_categories = db.query(func.count(Category.id)).scalar() or 0
    
    # Categories
    categories = db.query(Category).order_by(Category.name).all()
    
    # Destinations with ratings
    query = db.query(
        Destination,
        Category.name.label('category_name'),
        Category.icon.label('icon'),
        func.count(Review.id).label('review_count'),
        func.round(func.avg(Review.rating), 1).label('avg_rating')
    ).outerjoin(
        Category, Destination.category_id == Category.id
    ).outerjoin(
        Review, (Destination.id == Review.destination_id) & (Review.is_approved.is_(True))
    ).filter(
        Destination.is_active.is_(True)
    )
    
    if category and category > 0:
        query = query.filter(Destination.category_id == category)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Destination.name.like(search_term)) | 
            (Destination.description.like(search_term))
        )
    
    destinations_data = query.group_by(Destination.id).order_by(Destination.name).all()
    
    destinations = []
    for dest, cat_name, icon, review_count, avg_rating in destinations_data:
        destinations.append({
            'id': dest.id,
            'name': dest.name,
            'description': dest.description,
            'address': dest.address,
            'latitude': float(dest.latitude) if dest.latitude else None,
            'longitude': float(dest.longitude) if dest.longitude else None,
            'image_path': dest.image_path,
            'category_name': cat_name,
            'icon': icon,
            'review_count': review_count or 0,
            'avg_rating': float(avg_rating) if avg_rating else 0
        })
    
    all_destinations = db.query(Destination.id, Destination.name).filter(
        Destination.is_active.is_(True)
    ).order_by(Destination.name).all()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_destinations": total_destinations,
        "total_reviews": total_reviews,
        "total_categories": total_categories,
        "categories": categories,
        "destinations": destinations,
        "all_destinations": all_destinations,
        "category_filter": category,
        "search": search,
        "current_user": current_user,
        "UPLOAD_URL": UPLOAD_URL
    })


@app.get("/api/destinations")
async def get_destinations_api(
    category: Optional[int] = Query(0),
    search: Optional[str] = Query(""),
    db: Session = Depends(get_db)
):
    """API endpoint for destinations"""
    
    query = db.query(
        Destination,
        Category.name.label('category_name'),
        Category.icon.label('icon'),
        func.count(Review.id).label('review_count'),
        func.round(func.avg(Review.rating), 1).label('avg_rating')
    ).outerjoin(
        Category, Destination.category_id == Category.id
    ).outerjoin(
        Review, (Destination.id == Review.destination_id) & (Review.is_approved.is_(True))
    ).filter(
        Destination.is_active.is_(True)
    )
    
    if category and category > 0:
        query = query.filter(Destination.category_id == category)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Destination.name.like(search_term)) | 
            (Destination.description.like(search_term))
        )
    
    results = query.group_by(Destination.id).order_by(Destination.name).all()
    
    destinations = []
    for dest, cat_name, icon, review_count, avg_rating in results:
        destinations.append({
            'id': dest.id,
            'name': dest.name,
            'description': dest.description[:100] + '...' if dest.description else '',
            'latitude': float(dest.latitude) if dest.latitude else None,
            'longitude': float(dest.longitude) if dest.longitude else None,
            'image_path': f"{UPLOAD_URL}{dest.image_path}" if dest.image_path else None,
            'category_name': cat_name,
            'icon': icon,
            'review_count': review_count or 0,
            'avg_rating': float(avg_rating) if avg_rating else 0
        })
    
    return {"destinations": destinations}


@app.get("/api/routes")
async def get_routes_api(db: Session = Depends(get_db)):
    """API endpoint for transportation routes"""
    
    # Query routes with origin and destination names
    routes_query = db.query(
        Route,
        Destination.name.label('origin_name'),
    ).outerjoin(
        Destination, Route.origin_id == Destination.id
    ).filter(
        Route.is_active.is_(True)
    ).all()
    
    routes = []
    for route, origin_name in routes_query:
        # Get destination name separately
        dest_name = None
        if route.destination_id:
            dest = db.query(Destination.name).filter(Destination.id == route.destination_id).first()
            if dest:
                dest_name = dest[0]
        
        routes.append({
            'id': route.id,
            'route_name': route.route_name,
            'origin_id': route.origin_id,
            'origin_name': origin_name,
            'destination_id': route.destination_id,
            'destination_name': dest_name,
            'transport_mode': route.transport_mode,
            'distance_km': float(route.distance_km) if route.distance_km else None,
            'estimated_time_minutes': route.estimated_time_minutes,
            'base_fare': float(route.base_fare) if route.base_fare else 0,
            'fare_per_km': float(route.fare_per_km) if route.fare_per_km else 0,
            'description': route.description
        })
    
    return {"routes": routes}


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "service": "Tourism Guide System",
        "version": "2.0.0",
        "database": db_status
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )