from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL
from infrastructure.web import fetch_webpage
from infrastructure.db.source_repository import SourceRepository
from ingestion.services.webpage_parser_service import WebpageParserService
from config import logger

# NOTE: Solves the follow error:
# Cannot copy out of meta tensor; no data! Please use torch.nn.Module.to_empty() instead of torch.nn.Module.to() when moving module from meta to a different device.
embedding_model = SentenceTransformer(EMBEDDING_MODEL)


class WebpageIngestionService:
    def __init__(self, url: str, repository: SourceRepository):
        self.url = url
        self.repository = repository

    def process(self):
        try:
            logger.info("webpage_ingestion_service.process", url=self.url)
            self.__ingest_webpage()
        except Exception as e:
            logger.error(
                "webpage_ingestion_service.error",
                url=self.url,
                error=str(e),
            )
            raise e

    def __ingest_webpage(self):
        webpage = fetch_webpage(self.url)
        webpage_service = WebpageParserService(webpage)
        webpage_title = webpage_service.get_title()
        webpage_text = webpage_service.get_text()
        webpage_chunks = self.__format_chunks_from_webpage(webpage_text)
        embeddings = embedding_model.encode(webpage_chunks)

        with self.repository as repo:
            source = repo.get_or_create_source(webpage_title, self.url)
            repo.save_chunks(source, webpage_chunks, embeddings)

    def __format_chunks_from_webpage(self, text):
        return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
