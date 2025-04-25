import json
from config import WEBPAGES_LIST
from infrastructure.db.source_repository import SourceRepository
from ingestion.webpage_ingestion_service import WebpageIngestionService


def check_existing_index():
    with SourceRepository() as repo:
        if repo.has_chunks():
            print("✅ Index already exists in the database.")
            return True
    return False


def create_index():
    if check_existing_index():
        return

    print("📦 Ingesting data and generating embeddings...")

    urls = load_webpage_urls()
    with SourceRepository() as repo:
        for url in urls:
            WebpageIngestionService(url, repo).process()

    print("✅ Done. All chunks saved to the database.")


def load_webpage_urls():
    with open(WEBPAGES_LIST, "r", encoding="utf-8") as f:
        return json.load(f)
