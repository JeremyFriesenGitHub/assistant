from assistant import ask_question
from config.setup import setup

if __name__ == "__main__":
    setup()

    while True:
        q = input("\nAsk a question (or 'exit'): ")
        if q.lower() in {"exit", "quit"}:
            break
        ask_question(q)
