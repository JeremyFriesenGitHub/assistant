import pytest
from unittest.mock import MagicMock, patch
from agent import ResponseService


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
    return ResponseService(repository=fake_repository)


@patch("agent.services.response_service.create_completion", return_value="LLM Answer")
@patch("agent.services.response_service.create_prompt", return_value="Generated Prompt")
def test_ask_question(mock_create_prompt, mock_create_completion, service, capsys):
    """Should call the LLM with the correct prompt and print the answer."""

    service.ask_question("What is AI?", k=3)

    service.repository.get_top_k_chunks_by_similarity.assert_called_once_with(
        "What is AI?", 3
    )
    mock_create_prompt.assert_called_once_with(
        "Chunk 1\n\nChunk 2\n\nChunk 3", "What is AI?"
    )
    mock_create_completion.assert_called_once_with("Generated Prompt")
    captured = capsys.readouterr()
    assert "LLM Answer" in captured.out


def test_prepare_prompt_context(service):
    """Should prepare the prompt context correctly."""

    context = service._ResponseService__prepare_prompt_context("test query", k=3)

    assert context == "Chunk 1\n\nChunk 2\n\nChunk 3"
