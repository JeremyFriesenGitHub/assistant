import requests


def fetch_webpage_text(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise if status code isn't 200

    return response.text
