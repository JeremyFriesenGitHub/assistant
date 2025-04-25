from agent import Agent
from infrastructure.db.source_repository import SourceRepository

if __name__ == "__main__":
    with SourceRepository() as repository:
        agent = Agent(repository)

        while True:
            q = input("\nAsk a question (or 'exit'): ")
            if q.lower() in {"exit", "quit"}:
                break
            agent.ask_question(q)
