from .prompts import create_prompt
from infrastructure.ollama import create_llm_response
from infrastructure.db.source_repository import SourceRepository


class Agent:
    def __init__(self, repository: SourceRepository):
        self.repository = repository

    def ask_question(self, query, k=3):
        prompt_context = self.__prepare_prompt_context(query, k)

        print("\n🧠 Answering with context:\n")
        print(prompt_context)
        print("\n💬 LLM Answer:\n")

        answer = create_llm_response(create_prompt(prompt_context, query))
        print(answer)

    def __prepare_prompt_context(self, query, k):
        chunks = self.repository.get_top_k_chunks_by_similarity(query, k)
        context = "\n\n".join(chunk.content for chunk in chunks)
        return context
