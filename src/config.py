from sentence_transformers import SentenceTransformer


MARKDOWN_DIR = "data/markdown/faqs"
WEBPAGES_LIST = "data/webpages/list.json"
CHUNK_FILE = "data/chunks/chunks.txt"
INDEX_FILE = "data/embeddings/markdown_index.faiss"
OLLAMA_MODEL = "mistral"
OLLAMA_URL = "http://localhost:11434"
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
