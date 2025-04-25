ollama serve
ollama pull mistral
ollama run mistral


alembic -c src/infrastructure/db/alembic.ini revision --autogenerate -m "initial migration"
alembic -c src/infrastructure/db/alembic.ini upgrade head


PYTHONPATH=src celery -A infrastructure.celery worker --loglevel=info --pool=solo
PYTHONPATH=src celery -A infrastructure.celery worker --loglevel=info