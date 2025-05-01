import logging

logging.getLogger("sqlalchemy.engine.Engine").disabled = True

from completions import CompletionService
from infrastructure.db.source_repository import SourceRepository
from config.logger import logger
from result import Ok

if __name__ == "__main__":
    with SourceRepository() as repository:
        service = CompletionService(repository)

        while True:
            q = input("\nAsk a question (or 'exit'): ")
            if q.lower() in {"exit", "quit"}:
                break

            result = service.create(q)

            if isinstance(result, Ok):
                logger.info("dev_cli.answer_displayed", answer=result.ok_value)
                print(f"\nAnswer: {result.ok_value}")
            else:
                logger.error("dev_cli.answer_failed", error=repr(result.err_value))
                print(f"\nError: {result.err_value}")
