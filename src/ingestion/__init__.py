import json
from bs4 import BeautifulSoup
from config import WEBPAGES_LIST, EMBEDDING_MODEL
from infrastructure.web import fetch_webpage_text
from infrastructure.db.source_repository import SourceRepository


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
    for url in urls:
        fetch_and_ingest(url)

    print("✅ Done. All chunks saved to the database.")


def load_webpage_urls():
    with open(WEBPAGES_LIST, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_and_ingest(url):
    try:
        print(f"🌐 Fetching content from: {url}")
        ingest_webpage(url)
    except Exception as e:
        print(f"⚠️ Failed to fetch {url}: {e}")


def ingest_webpage(url):
    webpage_text = fetch_webpage_text(url)
    webpage_chunks = format_chunks_from_webpage_text(webpage_text)
    embeddings = EMBEDDING_MODEL.encode(webpage_chunks)

    with SourceRepository() as repo:
        source = repo.get_or_create_source(url)
        repo.save_chunks(source, webpage_chunks, embeddings)


def format_chunks_from_webpage_text(webpage_text):
    soup = BeautifulSoup(webpage_text, "html.parser")
    for tag in soup(
        ["script", "style", "header", "footer", "nav", "noscript", "svg", "form"]
    ):
        tag.decompose()
    text = soup.get_text(separator="\n")
    return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
