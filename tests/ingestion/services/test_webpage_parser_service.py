from bs4 import BeautifulSoup
from ingestion.services.webpage_parser_service import WebpageParserService


def test_get_title_returns_correct_title():
    """Should return the correct page title when a <title> tag is present."""

    html = "<html><head><title>Test Page</title></head><body><p>Hello World!</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")

    parser = WebpageParserService(soup)

    assert parser.get_title() == "Test Page"


def test_get_title_returns_none_when_no_title():
    """Should return None if there is no <title> tag."""

    html = "<html><head></head><body><p>Hello World!</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")

    parser = WebpageParserService(soup)

    assert parser.get_title() is None


def test_get_text_returns_cleaned_text():
    """Should remove layout elements (header, nav, footer, style) and keep only meaningful text."""

    html = """
    <html>
        <head><title>Ignore This</title><style>.hidden{}</style></head>
        <body>
            <header>Site Header</header>
            <nav>Navigation</nav>
            <p>Paragraph 1</p>
            <p>Paragraph 2</p>
            <footer>Footer Info</footer>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")

    parser = WebpageParserService(soup)
    text = parser.get_text()

    assert "Site Header" not in text
    assert "Navigation" not in text
    assert "Footer Info" not in text
    assert "Paragraph 1" in text
    assert "Paragraph 2" in text


def test_non_content_tags_are_removed():
    """Should remove script, style, SVG, and form elements from the page text."""

    html = """
    <html>
        <body>
            <script>console.log('hi')</script>
            <style>body { color: red; }</style>
            <svg><circle cx="50" cy="50" r="40" /></svg>
            <form><input type="text" /></form>
            <p>Real Content</p>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")

    parser = WebpageParserService(soup)
    text = parser.get_text()

    assert "console.log" not in text
    assert "color: red" not in text
    assert "circle" not in text
    assert "input" not in text
    assert "Real Content" in text
