# celery_config.py

from celery import Celery

# Create a Celery instance with a broker URL (e.g., Redis)
celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",  # Replace with your Redis URL
    backend="redis://localhost:6379/0"  # For storing results (optional)
)

# Optional: Configure Celery
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
