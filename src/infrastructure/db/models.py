from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    source = Column(String, nullable=False)
    embedding = Column(Vector(384), nullable=False)
