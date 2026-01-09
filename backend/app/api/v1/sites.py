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


@router.post("/{site_id}/test")
def test_scraping_rule(site_id: int, db: Session = Depends(get_db)):
    """
    Test scraping rule for a site
    """
    from app.services.rss_parser import validate_rss_feed
    from app.services.html_scraper import validate_html_selectors

    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Site with ID {site_id} not found"
        )

    if not site.scraping_rule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No scraping rule configured for this site"
        )

    rule = site.scraping_rule

    try:
        if rule.rule_type == "rss":
            if not rule.rss_url:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="RSS URL is required for RSS rule type"
                )
            result = validate_rss_feed(rule.rss_url)
        elif rule.rule_type == "css_selector":
            result = validate_html_selectors(
                url=site.url,
                list_container_selector=rule.list_container_selector,
                title_selector=rule.title_selector,
                link_selector=rule.link_selector,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported rule type: {rule.rule_type}"
            )

        return {
            "success": result['valid'],
            "message": result['message'],
            "posts_found": result['posts_count']
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "posts_found": 0
        }


@router.post("/{site_id}/scrape")
def scrape_site_now(site_id: int, db: Session = Depends(get_db)):
    """
    Manually trigger scraping for a site
    """
    from app.services.rss_parser import parse_rss_feed
    from app.services.html_scraper import scrape_html
    from app.models.post import Post
    from datetime import datetime

    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Site with ID {site_id} not found"
        )

    if not site.scraping_rule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No scraping rule configured for this site"
        )

    rule = site.scraping_rule

    try:
        # Scrape posts
        if rule.rule_type == "rss":
            if not rule.rss_url:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="RSS URL is required for RSS rule type"
                )
            scraped_posts = parse_rss_feed(rule.rss_url)
        elif rule.rule_type == "css_selector":
            scraped_posts = scrape_html(
                url=site.url,
                list_container_selector=rule.list_container_selector,
                title_selector=rule.title_selector,
                link_selector=rule.link_selector,
                date_selector=rule.date_selector,
                author_selector=rule.author_selector,
                excerpt_selector=rule.excerpt_selector,
                image_selector=rule.image_selector,
                date_format=rule.date_format,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported rule type: {rule.rule_type}"
            )

        # Save new posts to database
        new_posts_count = 0
        for post_data in scraped_posts:
            # Check if post already exists
            existing_post = db.query(Post).filter(
                Post.site_id == site.id,
                Post.url == post_data['url']
            ).first()

            if not existing_post:
                # Parse published_at
                published_at = None
                if post_data.get('published_at'):
                    try:
                        published_at = datetime.fromisoformat(post_data['published_at'])
                    except:
                        pass

                # Create new post
                new_post = Post(
                    site_id=site.id,
                    title=post_data['title'],
                    url=post_data['url'],
                    author=post_data.get('author'),
                    published_at=published_at,
                    excerpt=post_data.get('excerpt'),
                    image_url=post_data.get('image_url'),
                )
                db.add(new_post)
                new_posts_count += 1

        # Update site stats
        site.last_scraped_at = datetime.utcnow()
        if new_posts_count > 0 or len(scraped_posts) > 0:
            site.last_successful_scrape_at = datetime.utcnow()
            site.scrape_errors = 0

        db.commit()

        return {
            "success": True,
            "message": f"Successfully scraped {len(scraped_posts)} posts, {new_posts_count} new",
            "new_posts": new_posts_count,
            "total_posts": len(scraped_posts)
        }

    except Exception as e:
        # Update error count
        site.last_scraped_at = datetime.utcnow()
        site.scrape_errors += 1
        db.commit()

        return {
            "success": False,
            "message": str(e),
            "new_posts": 0
        }
