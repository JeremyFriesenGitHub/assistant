from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://myuser:mypassword@localhost:5445/mydatabase"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

# Ensure pgvector extension is enabled
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
