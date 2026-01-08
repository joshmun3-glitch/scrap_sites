"""Pydantic schemas"""
from app.schemas.site import (
    SiteBase,
    SiteCreate,
    SiteUpdate,
    SiteResponse,
    SiteWithStats,
    ScrapingRuleCreate,
    ScrapingRuleResponse,
)
from app.schemas.post import (
    PostBase,
    PostCreate,
    PostUpdate,
    PostResponse,
    PostWithSite,
    PostFilters,
    PaginatedPosts,
)

__all__ = [
    # Site schemas
    "SiteBase",
    "SiteCreate",
    "SiteUpdate",
    "SiteResponse",
    "SiteWithStats",
    "ScrapingRuleCreate",
    "ScrapingRuleResponse",
    # Post schemas
    "PostBase",
    "PostCreate",
    "PostUpdate",
    "PostResponse",
    "PostWithSite",
    "PostFilters",
    "PaginatedPosts",
]

