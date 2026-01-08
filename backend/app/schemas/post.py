"""
Post schemas for request/response validation
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class PostBase(BaseModel):
    """Base post schema"""
    title: str = Field(..., min_length=1, max_length=500)
    url: str = Field(..., max_length=1000)
    author: Optional[str] = Field(None, max_length=255)
    excerpt: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    published_at: Optional[datetime] = None
    tags: Optional[List[str]] = None


class PostCreate(PostBase):
    """Schema for creating a new post"""
    site_id: int


class PostUpdate(BaseModel):
    """Schema for updating a post"""
    is_read: Optional[bool] = None
    is_starred: Optional[bool] = None
    tags: Optional[List[str]] = None


class PostResponse(PostBase):
    """Schema for post response"""
    id: int
    site_id: int
    discovered_at: datetime
    is_read: bool
    is_starred: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostWithSite(PostResponse):
    """Schema for post with site information"""
    site: Optional[dict] = Field(None, description="Site information (id, name, favicon_url)")


class PostFilters(BaseModel):
    """Schema for post filtering"""
    site_id: Optional[int] = None
    is_read: Optional[bool] = None
    is_starred: Optional[bool] = None
    search_query: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    tags: Optional[List[str]] = None
    sort_by: str = Field(default="published_at", description="Sort by: published_at, discovered_at, title")
    sort_order: str = Field(default="desc", description="Sort order: asc, desc")


class PaginatedPosts(BaseModel):
    """Schema for paginated posts response"""
    posts: List[PostWithSite]
    total: int
    page: int
    page_size: int
    total_pages: int
