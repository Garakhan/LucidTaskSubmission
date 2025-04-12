from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserLogin, TokenResponse
from app.services.auth_service import create_user, authenticate_user
from app.db import SessionLocal

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    token = create_user(user, db)
    return {"access_token": token}

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(user, db)
    return {"access_token": token}
