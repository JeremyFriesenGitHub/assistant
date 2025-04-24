ollama serve
ollama pull mistral
ollama run mistral


alembic -c infrastructure/db/alembic.ini revision --autogenerate -m "initial migration"
alembic -c infrastructure/db/alembic.ini upgrade head
