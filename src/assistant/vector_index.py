import os
import faiss
import numpy as np
import json
from config import INDEX_FILE, CHUNK_FILE, WEBPAGES_LIST
from .markdown_loader import extract_chunks_from_markdown
from .webpage_loader import fetch_webpage_text
from infrastructure.db import SessionLocal
from infrastructure.db.models import Chunk, Source


def ensure_index_exists(model):
    if not os.path.exists(INDEX_FILE):
        print("📦 Building index from Markdown...")
        chunks = extract_chunks_from_markdown()

        with open(WEBPAGES_LIST, "r", encoding="utf-8") as f:
            urls = json.load(f)
            for url in urls:
                print(f"🌐 Fetching content from: {url}")
                try:
                    webpage_chunks = fetch_webpage_text(url)
                    save_chunks_with_source(model, url, webpage_chunks)
                except Exception as e:
                    print(f"⚠️ Failed to fetch {url}: {e}")

        print("✅ Done. You can now ask questions.")


def save_chunks_with_source(model, reference, chunks):
    session = SessionLocal()

    try:
        # Create or get source
        source = session.query(Source).filter_by(reference=reference).first()
        if not source:
            source = Source(
                name=reference.split("/")[-1], type="webpage", reference=reference
            )
            session.add(source)
            session.commit()
            session.refresh(source)

        # Build or load FAISS index
        embeddings = model.encode(chunks)
        dim = embeddings[0].shape[0]
        index = (
            faiss.read_index(INDEX_FILE)
            if os.path.exists(INDEX_FILE)
            else faiss.IndexFlatL2(dim)
        )

        for content, embedding in zip(chunks, embeddings):
            chunk = Chunk(content=content.strip(), source=source, embedding=embedding)
            session.add(chunk)
            index.add(np.array([embedding]))

        session.commit()
        faiss.write_index(index, INDEX_FILE)

        # Save raw chunks to CHUNK_FILE (for debug/logging)
        with open(CHUNK_FILE, "a", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(chunk.replace("\n", " ") + "\n")

    except Exception as e:
        session.rollback()
        print(f"❌ Failed to save chunks for {reference}: {e}")
    finally:
        session.close()


def read_index():
    return faiss.read_index(INDEX_FILE)
