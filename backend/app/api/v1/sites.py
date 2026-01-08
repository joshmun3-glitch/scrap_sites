"""
Sites API endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.site import Site
from app.models.scraping_rule import ScrapingRule
from app.schemas.site import SiteCreate, SiteUpdate, SiteResponse

router = APIRouter()


@router.post("/", response_model=SiteResponse, status_code=status.HTTP_201_CREATED)
def create_site(site_data: SiteCreate, db: Session = Depends(get_db)):
    """
    Create a new site with scraping rules
    """
    # Check if site with this URL already exists
    existing_site = db.query(Site).filter(Site.url == site_data.url).first()
    if existing_site:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Site with URL '{site_data.url}' already exists"
        )

    # Create site
    db_site = Site(
        name=site_data.name,
        url=site_data.url,
        site_type=site_data.site_type,
        description=site_data.description,
        scrape_interval_minutes=site_data.scrape_interval_minutes,
    )
    db.add(db_site)
    db.flush()  # Flush to get site.id

    # Create scraping rule
    scraping_rule_data = site_data.scraping_rule.model_dump()
    db_rule = ScrapingRule(
        site_id=db_site.id,
        **scraping_rule_data
    )
    db.add(db_rule)

    db.commit()
    db.refresh(db_site)

    return db_site


@router.get("/", response_model=List[SiteResponse])
def get_sites(
    is_active: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all sites with optional filtering
    """
    query = db.query(Site)

    if is_active is not None:
        query = query.filter(Site.is_active == is_active)

    sites = query.offset(skip).limit(limit).all()
    return sites


@router.get("/{site_id}", response_model=SiteResponse)
def get_site(site_id: int, db: Session = Depends(get_db)):
    """
    Get a specific site by ID
    """
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Site with ID {site_id} not found"
        )
    return site


@router.put("/{site_id}", response_model=SiteResponse)
def update_site(
    site_id: int,
    site_data: SiteUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a site
    """
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Site with ID {site_id} not found"
        )

    # Update site fields
    update_data = site_data.model_dump(exclude_unset=True, exclude={"scraping_rule"})
    for field, value in update_data.items():
        setattr(site, field, value)

    # Update scraping rule if provided
    if site_data.scraping_rule:
        if site.scraping_rule:
            # Update existing rule
            rule_data = site_data.scraping_rule.model_dump(exclude_unset=True)
            for field, value in rule_data.items():
                setattr(site.scraping_rule, field, value)
        else:
            # Create new rule
            rule_data = site_data.scraping_rule.model_dump()
            db_rule = ScrapingRule(site_id=site.id, **rule_data)
            db.add(db_rule)

    db.commit()
    db.refresh(site)

    return site


@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(site_id: int, db: Session = Depends(get_db)):
    """
    Delete a site
    """
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Site with ID {site_id} not found"
        )

    db.delete(site)
    db.commit()

    return None


@router.patch("/{site_id}/toggle", response_model=SiteResponse)
def toggle_site_active(site_id: int, db: Session = Depends(get_db)):
    """
    Toggle site active status
    """
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Site with ID {site_id} not found"
        )

    site.is_active = not site.is_active
    db.commit()
    db.refresh(site)

    return site
