# Carleton CS Assistant

*Description coming soon.*

## Setup Instructions

1. Install Ollama

```bash
brew install ollama
```

2. Pull the Mistral model

```bash
ollama serve
ollama pull mistral
```

3. Install Docker

Install Docker Desktop: https://www.docker.com/products/docker-desktop/

```bash
brew install docker-compose
```

4. Run Docker Compose

```bash
docker-compose up
```

5. Install More Stuff

```bash
brew install libpq && brew link --force libpq
brew install openssl@3
```

6. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

7. Install dependencies

```bash
env \
  LDFLAGS="-L/opt/homebrew/opt/openssl@3/lib" \
  CPPFLAGS="-I/opt/homebrew/opt/openssl@3/include" \
  PKG_CONFIG_PATH="/opt/homebrew/opt/openssl@3/lib/pkgconfig" \
  pip install -r requirements.txt
```

8. Run Migrations

```bash
alembic -c src/infrastructure/db/alembic.ini upgrade head
```


## Run Data Ingestion

In one terminal, activate your virtual environment and run Celery:

```bash
source venv/bin/activate
PYTHONPATH=src celery -A config.celery worker --loglevel=info --pool=solo
```

Then in another terminal run the data ingestion script:

```bash
source venv/bin/activate
make post-deploy
```

## Run Dev CLI

```bash
source venv/bin/activate
make dev
```

## Run Tests

```bash
source venv/bin/activate
make test
```