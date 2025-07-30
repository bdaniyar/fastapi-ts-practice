#!/bin/bash

alembic upgrade head

gunicorn fastapi_tasks_db.databasework.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000