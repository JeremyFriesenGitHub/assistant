from sentence_transformers import SentenceTransformer


WEBPAGES_LIST = "data/webpages/list.json"
OLLAMA_MODEL = "mistral"
OLLAMA_URL = "http://localhost:11434"
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
