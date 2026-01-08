"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base
from app.dependencies import get_db

# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database dependency override"""

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_site_data():
    """Sample site data for testing"""
    return {
        "name": "Test Blog",
        "url": "https://example.com",
        "site_type": "rss",
        "description": "A test blog",
        "scrape_interval_minutes": 30,
        "scraping_rule": {
            "rule_type": "rss",
            "rss_url": "https://example.com/feed"
        }
    }


@pytest.fixture
def sample_html_site_data():
    """Sample HTML site data for testing"""
    return {
        "name": "HTML Blog",
        "url": "https://htmlblog.com",
        "site_type": "html",
        "description": "An HTML blog",
        "scrape_interval_minutes": 60,
        "scraping_rule": {
            "rule_type": "css_selector",
            "list_container_selector": ".post-list",
            "title_selector": "h2.title",
            "link_selector": "a.link",
            "date_selector": "time.date",
            "author_selector": "span.author",
            "date_format": "%Y-%m-%d"
        }
    }
