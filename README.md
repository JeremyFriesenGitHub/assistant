# Carleton CS Assistant

*Description coming soon.*

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Set Up Ollama LLM

Start the Ollama server and pull the required model:

```bash
ollama serve
ollama pull mistral
ollama run mistral
```

## 3. Set Up the Database

Run Alembic to create and apply database migrations:

```bash
alembic -c src/infrastructure/db/alembic.ini revision --autogenerate -m "initial migration"
alembic -c src/infrastructure/db/alembic.ini upgrade head
```

> Make sure your database connection URL is properly configured in `src/infrastructure/db/alembic.ini` and your SQLAlchemy settings.

## 4. Run Celery Worker

Start the Celery worker to process tasks:

### Development (single-threaded)

```bash
PYTHONPATH=src celery -A infrastructure.celery worker --loglevel=info --pool=solo
```

### Production-like (multi-threaded)

```bash
PYTHONPATH=src celery -A infrastructure.celery worker --loglevel=info
```

## 5. Running Tests

Run the full test suite using Pytest:

```bash
PYTHONPATH=src pytest
```

## 6. Updating `requirements.txt`

After installing new packages, freeze your environment:

```bash
pip freeze > requirements.txt
```
