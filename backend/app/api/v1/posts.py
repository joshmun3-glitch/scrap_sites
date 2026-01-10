"""Posts API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.database import get_db
from app.models.post import Post
from app.schemas.post import PostResponse, PostListResponse
from datetime import datetime

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=PostListResponse)
def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    site_id: Optional[int] = None,
    is_read: Optional[bool] = None,
    is_starred: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get posts with filtering and pagination
    """
    query = db.query(Post)

    # Filters
    if site_id:
        query = query.filter(Post.site_id == site_id)
    if is_read is not None:
        query = query.filter(Post.is_read == is_read)
    if is_starred is not None:
        query = query.filter(Post.is_starred == is_starred)
    if search:
        query = query.filter(
            (Post.title.ilike(f"%{search}%")) |
            (Post.excerpt.ilike(f"%{search}%"))
        )

    # Get total count
    total = query.count()

    # Apply pagination and ordering
    posts = query.order_by(desc(Post.discovered_at)).offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "posts": posts
    }


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Get a specific post by ID
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found"
        )
    return post


@router.patch("/{post_id}/read", response_model=PostResponse)
def toggle_post_read(post_id: int, db: Session = Depends(get_db)):
    """
    Toggle post read status
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found"
        )

    post.is_read = not post.is_read
    if post.is_read and not post.read_at:
        post.read_at = datetime.utcnow()

    db.commit()
    db.refresh(post)
    return post


@router.patch("/{post_id}/star", response_model=PostResponse)
def toggle_post_star(post_id: int, db: Session = Depends(get_db)):
    """
    Toggle post starred status
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found"
        )

    post.is_starred = not post.is_starred
    db.commit()
    db.refresh(post)
    return post


@router.post("/bulk-read")
def mark_posts_as_read(
    post_ids: List[int],
    is_read: bool = True,
    db: Session = Depends(get_db)
):
    """
    Mark multiple posts as read/unread
    """
    posts = db.query(Post).filter(Post.id.in_(post_ids)).all()

    for post in posts:
        post.is_read = is_read
        if is_read and not post.read_at:
            post.read_at = datetime.utcnow()

    db.commit()

    return {
        "success": True,
        "updated_count": len(posts),
        "message": f"Successfully updated {len(posts)} posts"
    }


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Delete a post
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found"
        )

    db.delete(post)
    db.commit()

    return None
