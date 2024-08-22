# main.py
from app.schema.scrape_body import ScrapeRequest
from fastapi import FastAPI, BackgroundTasks
from app.tasks import scrape_youtube_data
from typing import List
from celery import group
from celery.result import AsyncResult
from app.celery_config import celery_app

app = FastAPI()


@app.post("/scrape")
def scrape_youtube_data_endpoint(request: ScrapeRequest):
    # Create a group of tasks, one for each URL
    task_group = group([scrape_youtube_data.s(item) for item in request.urls])

    # Run the group of tasks in parallel
    result = task_group.apply_async()

    # Map each URL to its corresponding task ID
    url_task_map = {item: task.id for item, task in zip(request.urls, result.results)}

    return {"url_task_map": url_task_map, "status": "Processing"}


@app.get("/status/{task_id}")
def get_task_status(task_id: str):
    # Get the task result using the task ID
    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.state == "PENDING":
        return {"task_id": task_id, "status": "Pending"}
    elif task_result.state == "SUCCESS":
        return {"task_id": task_id, "status": "Completed", "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"task_id": task_id, "status": "Failed", "error": str(task_result.info)}
    else:
        return {"task_id": task_id, "status": task_result.state}
