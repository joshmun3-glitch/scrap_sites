"""
Celery application initialization and configuration
"""
from celery import Celery
from app.config import get_settings

settings = get_settings()

# Create Celery instance
celery_app = Celery(
    "scracp_sites",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Seoul',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes timeout
    task_soft_time_limit=25 * 60,  # 25 minutes soft timeout
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,  # Prevent memory leaks
)

# Beat schedule: Run every 5 minutes
celery_app.conf.beat_schedule = {
    'check-and-scrape-sites-every-5-minutes': {
        'task': 'app.tasks.scraping_tasks.check_and_scrape_sites',
        'schedule': 300.0,  # 5 minutes in seconds
    },
}

# Auto-discover tasks
celery_app.autodiscover_tasks(['app.tasks'])
