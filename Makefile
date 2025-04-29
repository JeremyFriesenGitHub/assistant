cli:
	PYTHONPATH=src python src/apps/dev_cli.py

worker:
	PYTHONPATH=src celery -A config.celery worker --loglevel=info --pool=solo

test:
	PYTHONPATH=src pytest tests/

format:
	black src tests

lint:
	black --check src tests

post-deploy:
	PYTHONPATH=src python scripts/ingest_webpages_list.py
