import os
from pathlib import Path
from bs4 import BeautifulSoup
import faiss
from markdown import markdown
import numpy as np
from sentence_transformers import SentenceTransformer
from config import CHUNK_FILE, INDEX_FILE, MARKDOWN_DIR


def setup():
    if not os.path.exists(INDEX_FILE):
        print("📦 Building index from Markdown...")
        chunks = load_markdown_chunks()
        build_index(chunks)
        print("✅ Done. You can now ask questions.")


def load_markdown_chunks():
    chunks = []
    for path in Path(MARKDOWN_DIR).rglob("*.md"):
        text = extract_text_from_md(path)
        chunks += [c.strip() for c in text.split("\n\n") if c.strip()]
    return chunks


def extract_text_from_md(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = markdown(f.read())
    return BeautifulSoup(html, "html.parser").get_text()


def build_index(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)
    dim = embeddings[0].shape[0]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    faiss.write_index(index, INDEX_FILE)
    with open(CHUNK_FILE, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk.replace("\n", " ") + "\n")
