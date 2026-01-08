"""
Site model - represents a monitored website
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Site(Base):
    """Site model for storing monitored websites"""

    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False, unique=True, index=True)
    site_type = Column(String(50), nullable=False)  # 'rss' or 'html'
    description = Column(Text, nullable=True)
    favicon_url = Column(String(500), nullable=True)

    # Status and activity
    is_active = Column(Boolean, default=True, index=True)
    scrape_interval_minutes = Column(Integer, default=30)
    last_scraped_at = Column(DateTime(timezone=True), nullable=True, index=True)
    last_successful_scrape_at = Column(DateTime(timezone=True), nullable=True)
    scrape_errors = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    scraping_rule = relationship("ScrapingRule", back_populates="site", uselist=False, cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="site", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Site(id={self.id}, name='{self.name}', url='{self.url}')>"
