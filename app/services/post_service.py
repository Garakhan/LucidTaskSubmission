from sqlalchemy.orm import Session
from app.models.post_model import Post
from app.schemas.post_schema import PostCreate
from fastapi import HTTPException
from app.utils.cache_utils import get_cached_posts, cache_user_posts

def add_post(post_data: PostCreate, user_id: int, db: Session) -> int:
    """Add a new post for the authenticated user."""
    new_post = Post(text=post_data.text, user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # Invalidate user's post cache after adding
    cache_user_posts(user_id, None)
    return new_post.id

def get_user_posts(user_id: int, db: Session):
    """Return user's posts from cache if available, else fetch from DB and cache."""
    cached = get_cached_posts(user_id)
    if cached:
        return cached

    posts = db.query(Post).filter(Post.user_id == user_id).all()
    cache_user_posts(user_id, posts)
    return posts

def delete_post(post_id: int, user_id: int, db: Session):
    """Delete a post if it belongs to the authenticated user."""
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()

    # Invalidate cache
    cache_user_posts(user_id, None)
