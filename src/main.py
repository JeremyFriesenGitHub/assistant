from assistant import Assistant
from ingestion.vector_index import ensure_index_exists

if __name__ == "__main__":
    ensure_index_exists()
    assistant = Assistant()

    while True:
        q = input("\nAsk a question (or 'exit'): ")
        if q.lower() in {"exit", "quit"}:
            break
        assistant.ask_question(q)
