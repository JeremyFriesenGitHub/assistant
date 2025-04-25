from infrastructure.ollama import create_llm_response
from config import EMBEDDING_MODEL
from ingestion.markdown_loader import load_chunks
from ingestion.vector_index import read_index
from .prompts import create_prompt


class Assistant:
    def __init__(self):
        self.chunks = load_chunks()
        self.index = read_index()

    def ask_question(self, query, k=3):
        prompt_context = self.__prepare_prompt_context(query)

        print("\n🧠 Answering with context:\n")
        print(prompt_context)
        print("\n💬 LLM Answer:\n")

        answer = create_llm_response(create_prompt(prompt_context, query))
        print(answer)

    def __prepare_prompt_context(self, query):
        query_vec = EMBEDDING_MODEL.encode([query])
        _, I = self.index.search(query_vec, 3)
        retrieved = [self.chunks[i] for i in I[0]]
        context = "\n\n".join(retrieved)
        return context
