from pathlib import Path
from bs4 import BeautifulSoup
from markdown import markdown
from config import CHUNK_FILE, MARKDOWN_DIR


def extract_chunks_from_markdown():
    chunks = []
    for path in Path(MARKDOWN_DIR).rglob("*.md"):
        with open(path, "r", encoding="utf-8") as f:
            html = markdown(f.read())
        text = BeautifulSoup(html, "html.parser").get_text()
        chunks += [c.strip() for c in text.split("\n\n") if c.strip()]
    return chunks


def load_chunks():
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        return f.read().splitlines()
