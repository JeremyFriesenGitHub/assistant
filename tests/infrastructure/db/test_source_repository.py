import pytest
from unittest.mock import patch, MagicMock
from infrastructure.db.models import Source
from infrastructure.db.source_repository import (
    SourceRepository,
)


@pytest.fixture
def fake_session():
    return MagicMock()


@pytest.fixture
def repo(fake_session):
    with patch(
        "infrastructure.db.source_repository.SessionLocal", return_value=fake_session
    ):
        yield SourceRepository()


def test_has_chunks_true(fake_session, repo):
    """Should return True if a chunk exists."""
    fake_session.query.return_value.first.return_value = True
    assert repo.has_chunks() is True


def test_has_chunks_false(fake_session, repo):
    """Should return False if no chunks exist."""
    fake_session.query.return_value.first.return_value = None
    assert repo.has_chunks() is False


def test_get_or_create_source_existing(fake_session, repo):
    """Should return existing source if found."""
    fake_source = MagicMock()
    fake_session.query.return_value.filter_by.return_value.first.return_value = (
        fake_source
    )

    source = repo.get_or_create_source("Test Source", "http://example.com")

    assert source == fake_source
    fake_session.add.assert_not_called()
    fake_session.commit.assert_not_called()


def test_get_or_create_source_new(fake_session, repo):
    """Should create and return a new source if not found."""
    fake_session.query.return_value.filter_by.return_value.first.return_value = None

    source = repo.get_or_create_source("New Source", "http://newsite.com")

    assert isinstance(source, Source)
    fake_session.add.assert_called_once()
    fake_session.commit.assert_called_once()
    fake_session.refresh.assert_called_once_with(source)


def test_save_chunks(fake_session, repo):
    """Should add chunks and commit them."""
    fake_source = MagicMock()
    chunks = ["chunk one", "chunk two"]
    embeddings = [[0.1] * 384, [0.2] * 384]

    repo.save_chunks(fake_source, chunks, embeddings)

    # Should add two chunks
    assert fake_session.add.call_count == 2
    fake_session.commit.assert_called_once()


@patch("infrastructure.db.source_repository.SentenceTransformer")
def test_get_top_k_chunks_by_similarity(mock_transformer, fake_session, repo):
    """Should query top K chunks by similarity."""
    # Mock SentenceTransformer.encode
    mock_model_instance = MagicMock()
    mock_model_instance.encode.return_value = [[0.5] * 384]
    mock_transformer.return_value = mock_model_instance

    # Mock session.execute
    fake_execute_result = MagicMock()
    fake_execute_result.scalars.return_value.all.return_value = ["chunk1", "chunk2"]
    fake_session.execute.return_value = fake_execute_result

    chunks = repo.get_top_k_chunks_by_similarity("What is AI?", k=2)

    mock_model_instance.encode.assert_called_once_with(["What is AI?"])
    fake_session.execute.assert_called_once()
    assert chunks == ["chunk1", "chunk2"]
