from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import secrets

from config.database import get_db, User

# Security Configuration
SECRET_KEY = secrets.token_urlsafe(32)  # Generate a random secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Templates
templates = Jinja2Templates(directory="templates")

# Router
router = APIRouter()


# Helper Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    token = request.cookies.get("access_token")
    
    if not token:
        return None
    
    try:
        # Remove Bearer prefix if present
        if token.startswith("Bearer "):
            token = token[7:]
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_raw = payload.get("sub")
        
        if user_id_raw is None:
            return None
        
        # FIXED: Handle both string and int conversion
        try:
            user_id = int(user_id_raw)
        except (ValueError, TypeError):
            print(f"Invalid user_id format: {user_id_raw}")
            return None
        
        # Convert to int safely - handle both string and int
        try:
            user_id = int(user_id_raw)
        except (ValueError, TypeError):
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user
    
    except JWTError:
        return None
    except Exception as e:
        # Log the error for debugging
        print(f"Error in get_current_user: {str(e)}")
        return None


def require_login(request: Request, db: Session = Depends(get_db)) -> User:
    """Dependency that requires user to be logged in"""
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user


def require_admin(request: Request, db: Session = Depends(get_db)) -> User:
    """Dependency that requires user to be admin"""
    user = require_login(request, db)
    user_role = str(user.role) if hasattr(user, 'role') else 'user'
    if user_role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user


# Routes
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Display login/register page"""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": None,
        "success": None
    })


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Process login form"""
    
    # Find user
    user = db.query(User).filter(User.username == username).first()
    
    # Verify user exists
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username or password",
            "success": None
        })
    
    # Get the hashed password value - handle both direct access and string conversion
    try:
        stored_password = str(user.password) if hasattr(user.password, '__str__') else user.password
    except Exception:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Authentication error. Please try again.",
            "success": None
        })
    
    # Verify password
    if not verify_password(password, stored_password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username or password",
            "success": None
        })
    
    # Create access token - ensure user.id is converted to string for JWT
    user_id_str = str(user.id) if hasattr(user, 'id') else str(user[0])
    user_role_str = str(user.role) if hasattr(user, 'role') else str(user[4])
    access_token = create_access_token(data={"sub": user_id_str, "role": user_role_str})
    
    # Redirect based on role
    if str(user.role) == 'admin':
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
    else:
        response = RedirectResponse(url="/", status_code=303)
    
    # Set cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )
    
    return response


@router.post("/register")
async def register(
    request: Request,
    reg_username: str = Form(...),
    reg_email: str = Form(...),
    reg_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Process registration form"""
    
    # Check if username exists
    existing_user = db.query(User).filter(User.username == reg_username).first()
    if existing_user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Username already exists",
            "success": None
        })
    
    # Create new user
    hashed_password = get_password_hash(reg_password)
    new_user = User(
        username=reg_username,
        email=reg_email,
        password=hashed_password,
        role='user'
    )
    
    db.add(new_user)
    db.commit()
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": None,
        "success": "Registration successful! Please login."
    })


@router.get("/logout")
async def logout(request: Request):
    """Logout user and clear session"""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response


# User info endpoint
@router.get("/api/user/me")
async def get_current_user_info(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get current user information"""
    user = get_current_user(request, db)
    
    if not user:
        return {"logged_in": False}
    
    return {
        "logged_in": True,
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }