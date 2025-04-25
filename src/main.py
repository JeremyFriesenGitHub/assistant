from assistant import Assistant
from ingestion import create_index
from infrastructure.db.source_repository import SourceRepository

if __name__ == "__main__":
    with SourceRepository() as repository:
        assistant = Assistant(repository)

        while True:
            q = input("\nAsk a question (or 'exit'): ")
            if q.lower() in {"exit", "quit"}:
                break
            assistant.ask_question(q)
