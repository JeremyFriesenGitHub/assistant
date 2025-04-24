import requests
from config import OLLAMA_MODEL, OLLAMA_URL


def create_llm_response(prompt):
    res = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
    )
    return res.json()["response"]
