import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import INDEX_FILE, CHUNK_FILE
from infrastructure.ollama import create_llm_response


def ask_question(query, k=3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(INDEX_FILE)

    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        chunks = f.read().splitlines()

    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k)
    retrieved = [chunks[i] for i in I[0]]
    context = "\n\n".join(retrieved)

    print("\n🧠 Answering with context:\n")
    print(context)
    print("\n💬 LLM Answer:\n")
    answer = generate_answer_with_llm(context, query)
    print(answer)


def generate_answer_with_llm(context, query):
    prompt = f"""You are a helpful assistant answering user questions using only the provided FAQ content.

### Your instructions:
- Always start with: **"According to my sources..."**
- Respond in **Markdown format**
- **Only quote directly** from the context
- **Strongly emphasize any part labeled `Summary:`** — show it first if relevant
- Always cite the **FAQ file name** the quote came from
- Do **not** make anything up — use only the quotes provided

Context:
{context}

Question: {query}

Answer in markdown (with Summary emphasized first if found):
"""

    return create_llm_response(prompt)
