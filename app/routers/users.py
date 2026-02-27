from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.auth import (
    create_access_token,
    get_current_active_user,
    hash_password,
    verify_password,
)
from app.db import get_db
from app.models import User
from app.schemas import Token, UserCreate, UserResponse, UserUpdate

router = APIRouter(tags=["users"])


# ─── Auth ───────────────────────────────────────────────────────────────────

@router.post("/token", response_model=Token, summary="Login and get JWT token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return a JWT Bearer token."""
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# ─── User CRUD ───────────────────────────────────────────────────────────

@router.post("/users", response_model=UserResponse, status_code=201, summary="Register a new user")
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account. Passwords are hashed with bcrypt before storage."""
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users", response_model=List[UserResponse], summary="List all users")
def list_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Return a paginated list of users."""
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/users/me", response_model=UserResponse, summary="Get current user")
def get_me(current_user: User = Depends(get_current_active_user)):
    """Return the currently authenticated user."""
    return current_user


@router.get("/users/{user_id}", response_model=UserResponse, summary="Get user by ID")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Fetch a single user by their ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/me", response_model=UserResponse, summary="Update current user")
def update_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update the current user's username or email."""
    if user_in.username:
        existing = db.query(User).filter(User.username == user_in.username).first()
        if existing and existing.id != current_user.id:
            raise HTTPException(status_code=400, detail="Username already taken")
        current_user.username = user_in.username
    if user_in.email:
        existing = db.query(User).filter(User.email == user_in.email).first()
        if existing and existing.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email already taken")
        current_user.email = user_in.email
    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/users/me", status_code=204, summary="Delete current user")
def delete_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Permanently delete the current user account."""
    db.delete(current_user)
    db.commit()
