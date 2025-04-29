import pytest
from unittest.mock import MagicMock
from completions.services.context_generation_service import ContextGenerationService


@pytest.fixture
def fake_repository():
    repo = MagicMock()
    repo.get_top_k_chunks_by_similarity.return_value = [
        MagicMock(content="Chunk 1"),
        MagicMock(content="Chunk 2"),
        MagicMock(content="Chunk 3"),
    ]
    return repo


def test_generate_context_returns_joined_content(fake_repository):
    service = ContextGenerationService(
        query="example query", repository=fake_repository
    )
    context = service.process(k=3)

    fake_repository.get_top_k_chunks_by_similarity.assert_called_once_with(
        "example query", 3
    )
    assert context == "Chunk 1\n\nChunk 2\n\nChunk 3"


def test_generate_context_with_different_k(fake_repository):
    # Change fake_repository to return fewer chunks
    fake_repository.get_top_k_chunks_by_similarity.return_value = [
        MagicMock(content="Only Chunk 1"),
    ]
    service = ContextGenerationService(
        query="different query", repository=fake_repository
    )
    context = service.process(k=1)

    fake_repository.get_top_k_chunks_by_similarity.assert_called_once_with(
        "different query", 1
    )
    assert context == "Only Chunk 1"


def test_generate_context_when_no_chunks(fake_repository):
    # Make it return an empty list
    fake_repository.get_top_k_chunks_by_similarity.return_value = []
    service = ContextGenerationService(query="empty query", repository=fake_repository)
    context = service.process(k=3)

    fake_repository.get_top_k_chunks_by_similarity.assert_called_once_with(
        "empty query", 3
    )
    assert context == ""
