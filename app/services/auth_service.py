from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.auth_utils import hash_password, verify_password, create_access_token
from fastapi import HTTPException

def create_user(user_data: UserCreate, db: Session) -> str:
    """Register a new user and return JWT token."""
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"user_id": new_user.id})
    return token

def authenticate_user(user_data: UserLogin, db: Session) -> str:
    """Authenticate a user and return JWT token if valid."""
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"user_id": user.id})
    return token
