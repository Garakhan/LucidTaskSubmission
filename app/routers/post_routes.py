from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.schemas.post_schema import PostCreate, PostOut
from app.services.post_service import add_post, get_user_posts, delete_post
from app.utils.auth_utils import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

router = APIRouter(prefix="/posts", tags=["Posts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to extract and validate token
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid token scheme")

    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload["user_id"]

# Add Post
@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_user_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    post_id = add_post(post, user_id, db)
    return {"post_id": post_id}

# Get Posts
@router.get("/", response_model=List[PostOut])
def get_posts(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return get_user_posts(user_id, db)

# Delete Post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_post(
    post_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    delete_post(post_id, user_id, db)
    return
