import pytest
from dataclasses import dataclass
from completions.services.context_generation_service import ContextGenerationService


@dataclass
class FakeChunk:
    id: int
    content: str


@pytest.fixture
def fake_repository():
    class FakeRepository:
        def __init__(self):
            self._return_value = [
                FakeChunk(id=1, content="Chunk 1"),
                FakeChunk(id=2, content="Chunk 2"),
                FakeChunk(id=3, content="Chunk 3"),
            ]
            self.called_with = None

        def get_top_k_chunks_by_similarity(self, query, k):
            self.called_with = (query, k)
            return self._return_value

        def set_return_value(self, chunks):
            self._return_value = chunks

        def assert_called_once_with(self, query, k):
            assert self.called_with == (query, k)

    return FakeRepository()


def test_generate_context_returns_joined_content(fake_repository):
    service = ContextGenerationService(
        query="example query", repository=fake_repository
    )
    context = service.process(k=3)

    fake_repository.assert_called_once_with("example query", 3)
    assert context == "Chunk 1\n\nChunk 2\n\nChunk 3"


def test_generate_context_with_different_k(fake_repository):
    fake_repository.set_return_value(
        [
            FakeChunk(id=1, content="Only Chunk 1"),
        ]
    )

    service = ContextGenerationService(
        query="different query", repository=fake_repository
    )
    context = service.process(k=1)

    fake_repository.assert_called_once_with("different query", 1)
    assert context == "Only Chunk 1"


def test_generate_context_when_no_chunks(fake_repository):
    fake_repository.set_return_value([])

    service = ContextGenerationService(query="empty query", repository=fake_repository)
    context = service.process(k=3)

    fake_repository.assert_called_once_with("empty query", 3)
    assert context == ""
