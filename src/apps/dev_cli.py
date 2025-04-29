# NOTE: This application is intended to be run for development purposes only.

from completions import CompletionService
from infrastructure.db.source_repository import SourceRepository

if __name__ == "__main__":
    with SourceRepository() as repository:
        service = CompletionService(repository)

        while True:
            q = input("\nAsk a question (or 'exit'): ")
            if q.lower() in {"exit", "quit"}:
                break
            service.create(q)
