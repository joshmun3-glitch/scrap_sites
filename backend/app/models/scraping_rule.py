"""
Scraping Rule model - defines how to scrape each site
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ScrapingRule(Base):
    """Scraping rules for each site"""

    __tablename__ = "scraping_rules"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_type = Column(String(50), nullable=False)  # 'css_selector', 'xpath', 'rss'

    # RSS feed configuration
    rss_url = Column(String(500), nullable=True)

    # HTML scraping selectors
    list_container_selector = Column(String(500), nullable=True)
    title_selector = Column(String(500), nullable=True)
    link_selector = Column(String(500), nullable=True)
    date_selector = Column(String(500), nullable=True)
    author_selector = Column(String(500), nullable=True)
    excerpt_selector = Column(String(500), nullable=True)
    image_selector = Column(String(500), nullable=True)

    # Date parsing configuration
    date_format = Column(String(100), nullable=True)  # e.g., "%Y-%m-%d"
    date_attribute = Column(String(100), nullable=True)  # 'text', 'datetime', or custom attribute

    # Advanced options
    custom_headers = Column(JSON, nullable=True)  # Custom HTTP headers
    use_javascript = Column(Boolean, default=False)  # Whether to use headless browser
    wait_for_selector = Column(String(500), nullable=True)  # Selector to wait for (JS-rendered sites)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    site = relationship("Site", back_populates="scraping_rule")

    def __repr__(self):
        return f"<ScrapingRule(id={self.id}, site_id={self.site_id}, rule_type='{self.rule_type}')>"
