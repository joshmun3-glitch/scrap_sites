"""Tasks package"""
from app.tasks.celery_app import celery_app
from app.tasks import scraping_tasks

__all__ = ['celery_app', 'scraping_tasks']
