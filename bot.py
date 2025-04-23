import os
from pathlib import Path
from markdown import markdown
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ----- Settings -----
MARKDOWN_DIR = "data/markdown/faqs"
CHUNK_FILE = "data/chunks/markdown_chunks.txt"
INDEX_FILE = "data/embeddings/markdown_index.faiss"

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

# ----- Step 3: Ask questions -----
def ask_question(query, k=3):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index(INDEX_FILE)
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        chunks = f.read().splitlines()

    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k)
    results = [chunks[i] for i in I[0]]

    print("\n🔎 Most relevant chunks:\n")
    for r in results:
        print("-", r)
    print("\n💬 You can now generate an answer with an LLM using this context.")

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
