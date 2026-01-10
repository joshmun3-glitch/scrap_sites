"""
Site schemas for request/response validation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ScrapingRuleBase(BaseModel):
    """Base scraping rule schema"""
    rule_type: str = Field(..., description="Type of rule: 'rss', 'css_selector', or 'xpath'")
    rss_url: Optional[str] = None
    list_container_selector: Optional[str] = None
    title_selector: Optional[str] = None
    link_selector: Optional[str] = None
    date_selector: Optional[str] = None
    author_selector: Optional[str] = None
    excerpt_selector: Optional[str] = None
    image_selector: Optional[str] = None
    date_format: Optional[str] = None
    date_attribute: Optional[str] = "text"
    custom_headers: Optional[dict] = None
    use_javascript: bool = False
    wait_for_selector: Optional[str] = None


class ScrapingRuleCreate(ScrapingRuleBase):
    """Schema for creating scraping rule"""
    pass


class ScrapingRuleResponse(ScrapingRuleBase):
    """Schema for scraping rule response"""
    id: int
    site_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SiteBase(BaseModel):
    """Base site schema"""
    name: str = Field(..., min_length=1, max_length=255, description="Site name")
    url: str = Field(..., description="Site URL")
    site_type: str = Field(..., description="Site type: 'rss' or 'html'")
    description: Optional[str] = None
    scrape_interval_minutes: int = Field(default=30, ge=5, le=1440, description="Scraping interval in minutes")


class SiteCreate(SiteBase):
    """Schema for creating a new site"""
    scraping_rule: ScrapingRuleCreate


class SiteUpdate(BaseModel):
    """Schema for updating a site"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    url: Optional[str] = None
    site_type: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    scrape_interval_minutes: Optional[int] = Field(None, ge=5, le=1440)
    scraping_rule: Optional[ScrapingRuleCreate] = None


class SiteResponse(SiteBase):
    """Schema for site response"""
    id: int
    favicon_url: Optional[str] = None
    is_active: bool
    last_scraped_at: Optional[datetime] = None
    last_successful_scrape_at: Optional[datetime] = None
    scrape_errors: int
    created_at: datetime
    updated_at: datetime
    scraping_rule: Optional[ScrapingRuleResponse] = None

    class Config:
        from_attributes = True


class SiteStats(BaseModel):
    """Schema for site statistics"""
    total_posts: int
    new_posts_today: int
    new_posts_this_week: int
    last_post_date: Optional[datetime] = None
    avg_posts_per_day: float


class SiteWithStats(SiteResponse):
    """Schema for site with statistics"""
    stats: Optional[SiteStats] = None
