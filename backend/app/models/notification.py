"""
Notification model - user notifications
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Notification(Base):
    """Notification model for user alerts"""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)  # 'new_post', 'scrape_error', 'site_down'
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)

    # References
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"), nullable=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=True, index=True)

    # Status
    is_read = Column(Boolean, default=False, index=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<Notification(id={self.id}, type='{self.type}', title='{self.title}')>"
