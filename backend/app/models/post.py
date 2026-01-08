"""
Post model - represents discovered articles/posts
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Post(Base):
    """Post model for storing discovered articles"""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)

    # Post content
    title = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=False, unique=True, index=True)
    author = Column(String(255), nullable=True)
    excerpt = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)

    # Dates
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    discovered_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # User interactions
    is_read = Column(Boolean, default=False, index=True)
    is_starred = Column(Boolean, default=False, index=True)

    # Categorization
    tags = Column(JSON, nullable=True)  # JSON works in both PostgreSQL and SQLite

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    site = relationship("Site", back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title[:50]}...', url='{self.url}')>"
