from result import Ok, Result
from completions.prompts import create_prompt
from infrastructure.ollama import create_completion
from infrastructure.db.source_repository import SourceRepository
from completions.services.context_generation_service import ContextGenerationService
from config import logger


class CompletionService:
    def __init__(self, repository: SourceRepository):
        self.repository = repository

    def create(self, query: str, k: int = 3) -> Result[str, Exception]:
        logger.info("completion_service.create", query=query)

        prompt_context = ContextGenerationService(query, self.repository).process(k)
        logger.info("completion_service.context_generated", query=query)

        prompt = create_prompt(query, prompt_context)
        result = create_completion(prompt)

        if isinstance(result, Ok):
            logger.info(
                "completion_service.answer_generated",
                query=query,
                answer=result.ok_value[:10] + "...",
            )
        else:
            logger.error(
                "completion_service.answer_generation_error",
                query=query,
                error=result.err_value,
            )

        return result
