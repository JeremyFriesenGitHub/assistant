from ingestion.services.webpage_ingestion_service import WebpageIngestionService
from infrastructure.db.source_repository import SourceRepository
from infrastructure.celery import celery


@celery.task
def ingest_webpage(url):
    # print(f"[DEBUG] Would fetch: {url}")
    try:
        with SourceRepository() as repo:
            WebpageIngestionService(url, repo).process()
    except Exception as e:
        print(f"❌ Failed to ingest {url}: {e}")
