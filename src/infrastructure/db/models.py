from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(Enum("webpage", "file", name="source_type"), nullable=False)
    reference = Column(String, nullable=False, unique=True)

    chunks = relationship("Chunk", back_populates="source")


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    embedding = Column(Vector(384), nullable=False)

    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    source = relationship("Source", back_populates="chunks")
