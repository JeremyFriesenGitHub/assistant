import logging

logging.getLogger("sqlalchemy.engine.Engine").disabled = True

from celery import Celery

celery = Celery(
    "carleton_cs_bot_tasks",
    broker="redis://localhost:6370/0",
    backend="redis://localhost:6370/0",
)


# NOTE: This is a workaround to avoid the "No registered tasks" error.
# It is recommended to use the `autodiscover_tasks` method to automatically discover tasks.
# This is a workaround to avoid the "No registered tasks" error.
# celery.autodiscover_tasks(["ingestion.tasks"])

# ✅ Force Celery to load the task definitions
import ingestion.tasks.ingest_webpages_list_task
import ingestion.tasks.ingest_webpage_task
