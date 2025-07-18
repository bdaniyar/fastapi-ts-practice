from celery import Celery

from fastapi_tasks_db.databasework.config import settings

celery_app = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["fastapi_tasks_db.databasework.tasks.tasks"],
)
