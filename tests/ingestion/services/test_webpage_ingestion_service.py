from bs4 import BeautifulSoup
import pytest
from unittest.mock import patch, MagicMock

from ingestion.services.webpage_ingestion_service import WebpageIngestionService


@pytest.fixture
def fake_repository():
    repo = MagicMock()
    repo.get_or_create_source.return_value = "fake_source"
    repo.save_chunks.return_value = None
    repo.__enter__.return_value = repo
    repo.__exit__.return_value = None
    return repo


@pytest.fixture
def fake_webpage_html():
    return """
    <html>
        <head><title>Fake Page Title</title></head>
        <body>
            <p>First paragraph.</p>
            <p>Second paragraph.</p>
        </body>
    </html>
    """


@pytest.fixture
def setup_mocks(fake_webpage_html):
    with (
        patch(
            "ingestion.services.webpage_ingestion_service.fetch_webpage"
        ) as mock_fetch_webpage,
        patch(
            "ingestion.services.webpage_ingestion_service.embedding_model"
        ) as mock_embedding_model,
    ):
        # Setup fetch_webpage mock
        mock_fetch_webpage.return_value = BeautifulSoup(
            fake_webpage_html, "html.parser"
        )

        # Setup embedding_model mock
        mock_embedding_model.encode.return_value = [
            [0.1] * 384,
            [0.2] * 384,
            [0.3] * 384,
        ]

        yield {
            "mock_fetch_webpage": mock_fetch_webpage,
            "mock_embedding_model": mock_embedding_model,
        }


def test_fetch_webpage_called_with_correct_url(setup_mocks, fake_repository):
    service = WebpageIngestionService(
        url="https://fakeurl.com", repository=fake_repository
    )
    service.process()
    setup_mocks["mock_fetch_webpage"].assert_called_once_with("https://fakeurl.com")


def test_sentence_transformer_encodes_correct_chunks(setup_mocks, fake_repository):
    service = WebpageIngestionService(
        url="https://fakeurl.com", repository=fake_repository
    )
    service.process()

    setup_mocks["mock_embedding_model"].encode.assert_called_once()
    chunks_passed = setup_mocks["mock_embedding_model"].encode.call_args[0][0]
    assert chunks_passed == ["Fake Page Title", "First paragraph.", "Second paragraph."]


def test_repository_saves_chunks(setup_mocks, fake_repository):
    service = WebpageIngestionService(
        url="https://fakeurl.com", repository=fake_repository
    )
    service.process()

    fake_repository.get_or_create_source.assert_called_once_with(
        "Fake Page Title", "https://fakeurl.com"
    )
    fake_repository.save_chunks.assert_called_once()
