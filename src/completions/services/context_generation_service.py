from infrastructure.db.source_repository import SourceRepository


class ContextGenerationService:
    def __init__(self, query: str, repository: SourceRepository):
        self.query = query
        self.repository = repository

    def process(self, k=3):
        chunks = self.repository.get_top_k_chunks_by_similarity(self.query, k)
        context = "\n\n".join(chunk.content for chunk in chunks)
        return context
