# config/database.py
"""
Database Configuration for FastAPI Tourism Guide System
Connects to MySQL/MariaDB via XAMPP
FIXED: Added .env file loading
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, Boolean, DateTime, Enum, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, Mapped, mapped_column
from datetime import datetime
from typing import Generator, Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# FIXED: Load environment variables from .env file
load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")  # Default XAMPP password is empty
DB_NAME = os.getenv("DB_NAME", "tourism_guide")
DB_PORT = os.getenv("DB_PORT", "3306")

# Create Database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False  # Set to True for SQL query debugging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Base URL Configuration
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/")
UPLOAD_PATH = Path(__file__).parent.parent / "uploads"
UPLOAD_URL = f"{BASE_URL}uploads/"

# Create uploads directory if it doesn't exist
UPLOAD_PATH.mkdir(exist_ok=True)
(UPLOAD_PATH / "destinations").mkdir(exist_ok=True)
(UPLOAD_PATH / "categories").mkdir(exist_ok=True)

# Map Provider - FREE Leaflet/OpenStreetMap
MAP_PROVIDER = "leaflet"


# Database Models with proper type hints
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(Enum('admin', 'user'), default='user')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Destination(Base):
    __tablename__ = "destinations"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 8), nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(DECIMAL(11, 8), nullable=True)
    contact_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    opening_hours: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    entry_fee: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    rating: Mapped[Optional[float]] = mapped_column(DECIMAL(2, 1), default=0.0)
    image_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DestinationImage(Base):
    __tablename__ = "destination_images"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    destination_id: Mapped[int] = mapped_column(Integer, nullable=False)
    image_path: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Review(Base):
    __tablename__ = "reviews"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    destination_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    user_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Route(Base):
    __tablename__ = "routes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    route_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    origin_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    destination_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    transport_mode: Mapped[str] = mapped_column(Enum('jeepney', 'taxi', 'bus', 'van', 'tricycle', 'walking'), nullable=False)
    distance_km: Mapped[Optional[float]] = mapped_column(DECIMAL(6, 2), nullable=True)
    estimated_time_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    base_fare: Mapped[Optional[float]] = mapped_column(DECIMAL(8, 2), nullable=True)
    fare_per_km: Mapped[Optional[float]] = mapped_column(DECIMAL(8, 2), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WebsiteFeedback(Base):
    __tablename__ = "website_feedback"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    user_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(Enum('usability', 'features', 'content', 'design', 'general'), default='general')
    feedback: Mapped[str] = mapped_column(Text, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# Dependency to get database session
def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI endpoints
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Helper function to create tables
def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")


# Helper function to test database connection
def test_connection():
    """Test database connection"""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database connection successful!")
        print(f"   Connected to: {DB_NAME}@{DB_HOST}:{DB_PORT}")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"   Attempted connection: {DB_NAME}@{DB_HOST}:{DB_PORT}")
        return False