from sentence_transformers import SentenceTransformer
from infrastructure.ollama import create_llm_response
from .markdown_loader import load_chunks
from .vector_index import ensure_index_exists, read_index
from .prompts import create_prompt


class Assistant:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        ensure_index_exists(self.model)
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
        query_vec = self.model.encode([query])
        _, I = self.index.search(query_vec, 3)
        retrieved = [self.chunks[i] for i in I[0]]
        context = "\n\n".join(retrieved)
        return context
