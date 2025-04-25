import requests
from bs4 import BeautifulSoup


def fetch_webpage_text(url):
    """Fetches and chunks text content from a webpage."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise if status code isn't 200

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove non-content tags
    for tag in soup(
        ["script", "style", "header", "footer", "nav", "noscript", "svg", "form"]
    ):
        tag.decompose()

    # Extract the main text content
    text = soup.get_text(separator="\n")

    # Chunk by paragraph-like breaks
    chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    return chunks
