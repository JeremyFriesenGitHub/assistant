import logging

logging.getLogger("sqlalchemy.engine.Engine").disabled = True

from completions import CompletionService
from infrastructure.db.source_repository import SourceRepository
from config.logger import logger

if __name__ == "__main__":
    with SourceRepository() as repository:
        service = CompletionService(repository)

        while True:
            q = input("\nAsk a question (or 'exit'): ")
            if q.lower() in {"exit", "quit"}:
                break
            answer = service.create(q)
            logger.info("dev_cli.answer_displayed", answer=answer)
