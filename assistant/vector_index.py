import os
import faiss
import numpy as np
from config import INDEX_FILE, CHUNK_FILE
from .markdown_loader import extract_chunks_from_markdown


def ensure_index_exists(model):
    if not os.path.exists(INDEX_FILE):
        print("📦 Building index from Markdown...")
        chunks = extract_chunks_from_markdown()
        build_index(model, chunks)
        print("✅ Done. You can now ask questions.")


def build_index(model, chunks):
    embeddings = model.encode(chunks)
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    faiss.write_index(index, INDEX_FILE)

    with open(CHUNK_FILE, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk.replace("\n", " ") + "\n")


def read_index():
    return faiss.read_index(INDEX_FILE)
