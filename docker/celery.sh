#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery --app=fastapi_tasks_db.databasework.tasks.celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    celery --app=fastapi_tasks_db.databasework.tasks.celery flower
fi