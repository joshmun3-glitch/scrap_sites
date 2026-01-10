"""
Celery tasks for automatic site scraping
"""
from datetime import datetime, timedelta
from celery import group
from app.tasks.celery_app import celery_app
from app.database import SessionLocal
from app.models.site import Site
from app.models.post import Post
from app.services.rss_parser import parse_rss_feed
from app.services.html_scraper import scrape_html
import logging

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    name='app.tasks.scraping_tasks.check_and_scrape_sites',
    max_retries=3
)
def check_and_scrape_sites(self):
    """
    Check all active sites and scrape those that need updating
    - Checks scrape_interval_minutes for each site
    - Determines if scraping is needed based on last_scraped_at
    - Triggers parallel scraping for eligible sites
    """
    db = SessionLocal()
    try:
        sites = db.query(Site).filter(Site.is_active == True).all()
        sites_to_scrape = []
        now = datetime.utcnow()

        for site in sites:
            should_scrape = False

            if site.last_scraped_at is None:
                # Never scraped before
                should_scrape = True
            else:
                # Check if enough time has passed
                time_since_last = now - site.last_scraped_at
                interval = site.scrape_interval_minutes or 30

                if time_since_last >= timedelta(minutes=interval):
                    should_scrape = True

            if should_scrape:
                sites_to_scrape.append(site.id)
                logger.info(f"Site {site.id} ({site.name}) scheduled for scraping")

        if not sites_to_scrape:
            logger.info("No sites need scraping at this time")
            return {'status': 'success', 'sites_scraped': 0}

        # Execute parallel scraping
        logger.info(f"Starting parallel scraping for {len(sites_to_scrape)} sites")
        job = group(scrape_single_site.s(site_id) for site_id in sites_to_scrape)
        job.apply_async()

        return {
            'status': 'success',
            'sites_to_scrape': sites_to_scrape,
            'count': len(sites_to_scrape)
        }

    except Exception as e:
        logger.error(f"Error in check_and_scrape_sites: {str(e)}")
        raise self.retry(exc=e, countdown=60)
    finally:
        db.close()


@celery_app.task(
    bind=True,
    name='app.tasks.scraping_tasks.scrape_single_site',
    max_retries=3,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def scrape_single_site(self, site_id: int):
    """
    Scrape a single site
    - Performs RSS or HTML scraping based on rule type
    - Checks for duplicate posts before saving
    - Updates site statistics
    - Handles errors with retry logic (max 3 attempts, backoff strategy)

    Args:
        site_id: ID of the site to scrape

    Returns:
        Dict with status, site_id, total_posts, and new_posts count
    """
    db = SessionLocal()
    try:
        site = db.query(Site).filter(Site.id == site_id).first()

        if not site:
            logger.warning(f"Site {site_id} not found")
            return {'status': 'skipped', 'reason': 'not_found'}

        if not site.is_active:
            logger.info(f"Site {site_id} ({site.name}) is not active")
            return {'status': 'skipped', 'reason': 'inactive'}

        rule = site.scraping_rule

        if not rule:
            logger.warning(f"Site {site_id} ({site.name}) has no scraping rule")
            return {'status': 'skipped', 'reason': 'no_rule'}

        logger.info(f"Starting scrape for site {site_id} ({site.name})")
        scraped_posts = []

        # Execute scraping based on rule type
        if rule.rule_type == "rss":
            if not rule.rss_url:
                logger.error(f"Site {site_id} has RSS rule but no RSS URL")
                return {'status': 'error', 'reason': 'missing_rss_url'}

            scraped_posts = parse_rss_feed(rule.rss_url)
            logger.info(f"RSS scraping found {len(scraped_posts)} posts")

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
            logger.info(f"HTML scraping found {len(scraped_posts)} posts")
        else:
            logger.error(f"Unknown rule type: {rule.rule_type}")
            return {'status': 'error', 'reason': 'unknown_rule_type'}

        # Save new posts
        new_posts_count = 0
        for post_data in scraped_posts:
            # Check for duplicate
            existing = db.query(Post).filter(
                Post.site_id == site.id,
                Post.url == post_data['url']
            ).first()

            if not existing:
                # Parse published date
                published_at = None
                if post_data.get('published_at'):
                    try:
                        published_at = datetime.fromisoformat(post_data['published_at'])
                    except (ValueError, TypeError):
                        logger.warning(f"Could not parse date: {post_data.get('published_at')}")

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

        # Update site statistics
        site.last_scraped_at = datetime.utcnow()
        if len(scraped_posts) > 0:
            site.last_successful_scrape_at = datetime.utcnow()
            site.scrape_errors = 0

        db.commit()

        logger.info(
            f"Scraping complete for site {site_id} ({site.name}): "
            f"{new_posts_count} new posts out of {len(scraped_posts)} total"
        )

        return {
            'status': 'success',
            'site_id': site_id,
            'site_name': site.name,
            'total_posts': len(scraped_posts),
            'new_posts': new_posts_count,
        }

    except Exception as e:
        logger.error(f"Error scraping site {site_id}: {str(e)}")

        # Update error count
        try:
            site = db.query(Site).filter(Site.id == site_id).first()
            if site:
                site.last_scraped_at = datetime.utcnow()
                site.scrape_errors += 1
                db.commit()
        except Exception as update_error:
            logger.error(f"Could not update error count: {str(update_error)}")

        # Retry with backoff strategy
        if self.request.retries < self.max_retries:
            countdown = min(60 * (2 ** self.request.retries), 600)
            logger.info(f"Retrying site {site_id} in {countdown} seconds (attempt {self.request.retries + 1}/{self.max_retries})")
            raise self.retry(exc=e, countdown=countdown)

        return {
            'status': 'error',
            'site_id': site_id,
            'error': str(e)
        }

    finally:
        db.close()
