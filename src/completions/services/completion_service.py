from completions.prompts import create_prompt
from infrastructure.ollama import create_completion
from infrastructure.db.source_repository import SourceRepository
from completions.services.context_generation_service import ContextGenerationService


class CompletionService:
    def __init__(self, repository: SourceRepository):
        self.repository = repository

    def create(self, query, k=3):
        prompt_context = ContextGenerationService(query, self.repository).process(k)

        print("\n🧠 Answering with context:\n")
        print(prompt_context)
        print("\n💬 LLM Answer:\n")

        answer = create_completion(create_prompt(prompt_context, query))
        print(answer)
