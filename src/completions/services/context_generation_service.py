from config import logger
from infrastructure.db.source_repository import SourceRepository


class ContextGenerationService:
    def __init__(self, query: str, repository: SourceRepository):
        self.query = query
        self.repository = repository

    def process(self, k=3):
        logger.info("context_generation_service.process", query=self.query)

        chunks = self.repository.get_top_k_chunks_by_similarity(self.query, k)
        logger.info(
            "context_generation_service.found_context_chunks",
            chunk_ids=[chunk.id for chunk in chunks],
        )

        context = "\n\n".join(chunk.content for chunk in chunks)
        return context
