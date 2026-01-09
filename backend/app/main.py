"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api.v1 import sites, posts

settings = get_settings()

app = FastAPI(
    title="Site Monitor API",
    description="API for monitoring blogs and news sites for new posts",
    version="0.1.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sites.router, prefix="/api/v1/sites", tags=["sites"])
app.include_router(posts.router, prefix="/api/v1", tags=["posts"])


@app.get("/")
def read_root():
    """Root endpoint - health check"""
    return {
        "message": "Site Monitor API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
