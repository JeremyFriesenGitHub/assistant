from typing import List
import numpy as np
from sqlalchemy import select
from infrastructure.db import SessionLocal
from infrastructure.db.models import Chunk, Source
from config import EMBEDDING_MODEL


class SourceRepository:
    def __init__(self):
        self.session = SessionLocal()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def has_chunks(self) -> bool:
        return self.session.query(Chunk).first() is not None

    def get_or_create_source(self, reference: str) -> Source:
        source = self.session.query(Source).filter_by(reference=reference).first()
        if not source:
            source = Source(
                name=reference.split("/")[-1], type="webpage", reference=reference
            )
            self.session.add(source)
            self.session.commit()
            self.session.refresh(source)
        return source

    def save_chunks(self, source: Source, chunks: list[str], embeddings: list):
        for content, embedding in zip(chunks, embeddings):
            cleaned_content = content.replace("\n", " ").strip()
            chunk = Chunk(content=cleaned_content, source=source, embedding=embedding)
            self.session.add(chunk)
        self.session.commit()

    def get_top_k_chunks_by_similarity(self, query: str, k: int = 3) -> List[Chunk]:
        query_vector_embedding = EMBEDDING_MODEL.encode([query])[0]
        stmt = (
            select(Chunk)
            .order_by(Chunk.embedding.l2_distance(np.array(query_vector_embedding)))
            .limit(k)
        )
        return self.session.execute(stmt).scalars().all()
