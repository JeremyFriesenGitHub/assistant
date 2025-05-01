import requests
from result import Ok, Err, Result
from config import OLLAMA_MODEL, OLLAMA_URL


def create_completion(prompt: str) -> Result[str, Exception]:
    try:
        res = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=30,
        )
        res.raise_for_status()
        return Ok(res.json()["response"])
    except (requests.RequestException, ValueError, KeyError) as e:
        return Err(e)
