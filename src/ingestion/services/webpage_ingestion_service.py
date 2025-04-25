from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL
from infrastructure.web import fetch_webpage_text
from infrastructure.db.source_repository import SourceRepository


class WebpageIngestionService:
    def __init__(self, url: str, repository: SourceRepository):
        self.url = url
        self.repository = repository

    def process(self):
        try:
            print(f"🌐 Fetching content from: {self.url}")
            self.__ingest_webpage(self.url)
        except Exception as e:
            print(f"⚠️ Failed to fetch {self.url}: {e}")

    def __ingest_webpage(self, url):
        webpage_text = fetch_webpage_text(url)
        webpage_chunks = self.__format_chunks_from_webpage_text(webpage_text)
        embeddings = SentenceTransformer(EMBEDDING_MODEL).encode(webpage_chunks)

        with SourceRepository() as repo:
            source = repo.get_or_create_source(url)
            repo.save_chunks(source, webpage_chunks, embeddings)

    def __format_chunks_from_webpage_text(self, webpage_text):
        soup = BeautifulSoup(webpage_text, "html.parser")
        for tag in soup(
            ["script", "style", "header", "footer", "nav", "noscript", "svg", "form"]
        ):
            tag.decompose()
        text = soup.get_text(separator="\n")
        return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
