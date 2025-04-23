import os
from pathlib import Path
from markdown import markdown
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests

# ----- Settings -----
MARKDOWN_DIR = "data/markdown/faqs"
CHUNK_FILE = "data/chunks/markdown_chunks.txt"
INDEX_FILE = "data/embeddings/markdown_index.faiss"
OLLAMA_MODEL = "mistral"

# ----- Step 1: Load and clean Markdown -----
def extract_text_from_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = markdown(f.read())
    return BeautifulSoup(html, "html.parser").get_text()

def load_markdown_chunks():
    chunks = []
    for path in Path(MARKDOWN_DIR).rglob("*.md"):
        text = extract_text_from_md(path)
        chunks += [c.strip() for c in text.split("\n\n") if c.strip()]
    return chunks

# ----- Step 2: Embed and index -----
def build_index(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)
    dim = embeddings[0].shape[0]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    faiss.write_index(index, INDEX_FILE)
    with open(CHUNK_FILE, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk.replace("\n", " ") + "\n")

def generate_answer_with_llm(context, query, model=OLLAMA_MODEL):
    prompt = f"""You are a helpful assistant answering user questions using only the provided FAQ content.

### Your instructions:
- Always start with: **"According to my sources..."**
- Respond in **Markdown format**
- **Only quote directly** from the context
- **Strongly emphasize any part labeled `Summary:`** — show it first if relevant
- Always cite the **FAQ file name** the quote came from
- Do **not** make anything up — use only the quotes provided

Here is the context (each section includes the source file name):

{context}

Question: {query}

Answer in markdown (with Summary emphasized first if found):
"""

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
    )
    return res.json()["response"]

# ----- Step 4: Ask questions -----
def ask_question(query, k=3):
    model = SentenceTransformer('all-MiniLM-L6-v2')
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

# ----- Entrypoint -----
if __name__ == "__main__":
    if not os.path.exists(INDEX_FILE):
        print("📦 Building index from Markdown...")
        chunks = load_markdown_chunks()
        build_index(chunks)
        print("✅ Done. You can now ask questions.")

    while True:
        q = input("\nAsk a question (or 'exit'): ")
        if q.lower() in {"exit", "quit"}:
            break
        ask_question(q)
