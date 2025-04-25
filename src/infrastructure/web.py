from bs4 import BeautifulSoup
import requests


def fetch_webpage(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise if status code isn't 200

    return BeautifulSoup(response.text, "html.parser")
