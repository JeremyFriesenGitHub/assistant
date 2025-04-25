import json

from config import WEBPAGES_LIST
from .ingest_webpage_task import ingest_webpage  # the actual task
from services.celery import celery


@celery.task
def ingest_webpages_list():
    print("📦 Queuing webpage ingestion tasks...")

    with open(WEBPAGES_LIST, "r", encoding="utf-8") as f:
        urls = json.load(f)

    for url in urls:
        ingest_webpage.delay(url)  # 🔥 spawn a task per URL

    print("✅ All tasks dispatched.")
