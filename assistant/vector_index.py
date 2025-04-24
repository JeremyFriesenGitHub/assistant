import os
import faiss
import numpy as np
from config import INDEX_FILE, CHUNK_FILE, WEBPAGES_LIST
from .markdown_loader import extract_chunks_from_markdown
from .webpage_loader import fetch_webpage_text
import json


def ensure_index_exists(model):
    if not os.path.exists(INDEX_FILE):
        print("📦 Building index from Markdown...")
        chunks = extract_chunks_from_markdown()

        with open(WEBPAGES_LIST, "r", encoding="utf-8") as f:
            urls = json.load(f)
            for url in urls:
                print(f"🌐 Fetching content from: {url}")
                try:
                    for chunk in fetch_webpage_text(url):
                        chunks.append(f"[source:{url}] {chunk}")
                except Exception as e:
                    print(f"⚠️ Failed to fetch {url}: {e}")

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
