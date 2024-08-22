# tasks.py
from app.services.get_youtube_data_service import GetYouTubeDataService
from app.celery_config import celery_app


@celery_app.task
def scrape_youtube_data(url):
    return GetYouTubeDataService(url=url).gather_youtube_data_and_save()
