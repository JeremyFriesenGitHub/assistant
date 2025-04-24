from assistant import Assistant

if __name__ == "__main__":
    assistant = Assistant()

    while True:
        q = input("\nAsk a question (or 'exit'): ")
        if q.lower() in {"exit", "quit"}:
            break
        assistant.ask_question(q)
