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
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password hashing - Support both $2b$ (Python) and $2y$ (PHP) bcrypt formats
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Templates
templates = Jinja2Templates(directory="templates")

# Router
router = APIRouter()


# Helper Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash - handles both $2b$ (Python) and $2y$ (PHP) bcrypt"""
    try:
        # Convert PHP's $2y$ bcrypt to Python's $2b$ format
        if hashed_password.startswith('$2y$'):
            hashed_password = '$2b$' + hashed_password[4:]
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
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
    """Get current logged-in user from JWT token"""
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
        
        # Convert to int safely
        try:
            user_id = int(user_id_raw)
        except (ValueError, TypeError):
            print(f"Invalid user_id format: {user_id_raw}")
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user
    
    except JWTError as e:
        print(f"JWT Error: {e}")
        return None
    except Exception as e:
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
    
    print(f"🔐 Login attempt for username: {username}")
    
    # Find user
    user = db.query(User).filter(User.username == username).first()
    
    # Verify user exists
    if not user:
        print(f"❌ User not found: {username}")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username or password",
            "success": None
        })
    
    # Get the hashed password
    try:
        stored_password = str(user.password)
        print(f"🔑 Password hash found (first 20 chars): {stored_password[:20]}...")
    except Exception as e:
        print(f"❌ Error getting password: {e}")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Authentication error. Please try again.",
            "success": None
        })
    
    # Verify password
    print(f"🔍 Verifying password...")
    if not verify_password(password, stored_password):
        print(f"❌ Password verification failed for user: {username}")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username or password",
            "success": None
        })
    
    print(f"✅ Login successful for user: {username}, role: {user.role}")
    
    # Create access token
    user_id_str = str(user.id)
    user_role_str = str(user.role)
    access_token = create_access_token(data={"sub": user_id_str, "role": user_role_str})
    
    # Redirect based on role
    if user_role_str == 'admin':
        print(f"➡️  Redirecting to admin dashboard")
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
    else:
        print(f"➡️  Redirecting to homepage")
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
    
    print(f"📝 Registration attempt for username: {reg_username}")
    
    # Check if username exists
    existing_user = db.query(User).filter(User.username == reg_username).first()
    if existing_user:
        print(f"❌ Username already exists: {reg_username}")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Username already exists",
            "success": None
        })
    
    # Create new user
    hashed_password = get_password_hash(reg_password)
    print(f"🔐 Creating new user with hashed password")
    
    new_user = User(
        username=reg_username,
        email=reg_email,
        password=hashed_password,
        role='user'
    )
    
    db.add(new_user)
    db.commit()
    
    print(f"✅ Registration successful for: {reg_username}")
    
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
    print("👋 User logged out")
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