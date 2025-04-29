import pytest
from unittest.mock import MagicMock, patch
from completions import CompletionService


@pytest.fixture
def fake_repository():
    repo = MagicMock()
    repo.get_top_k_chunks_by_similarity.return_value = [
        MagicMock(content="Chunk 1"),
        MagicMock(content="Chunk 2"),
        MagicMock(content="Chunk 3"),
    ]
    return repo


@pytest.fixture
def service(fake_repository):
    return CompletionService(repository=fake_repository)


@patch(
    "completions.services.completion_service.create_completion",
    return_value="LLM Answer",
)
@patch(
    "completions.services.completion_service.create_prompt",
    return_value="Generated Prompt",
)
def test_create(mock_create_prompt, mock_create_completion, service, capsys):
    """Should call the LLM with the correct prompt and print the answer."""

    service.create("What is AI?", k=3)

    service.repository.get_top_k_chunks_by_similarity.assert_called_once_with(
        "What is AI?", 3
    )
    mock_create_prompt.assert_called_once_with(
        "Chunk 1\n\nChunk 2\n\nChunk 3", "What is AI?"
    )
    mock_create_completion.assert_called_once_with("Generated Prompt")

    captured = capsys.readouterr()
    assert "LLM Answer" in captured.out
