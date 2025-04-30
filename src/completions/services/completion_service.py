from completions.prompts import create_prompt
from infrastructure.ollama import create_completion
from infrastructure.db.source_repository import SourceRepository
from completions.services.context_generation_service import ContextGenerationService
from config import logger


class CompletionService:
    def __init__(self, repository: SourceRepository):
        self.repository = repository

    def create(self, query, k=3):
        logger.info("completion_service.create", query=query)

        prompt_context = ContextGenerationService(query, self.repository).process(k)
        logger.info("completion_service.context_generated", query=query)

        answer = create_completion(create_prompt(prompt_context, query))
        logger.info(
            "completion_service.answer_generated",
            query=query,
            answer=answer[0:10] + "...",
        )
        return answer
