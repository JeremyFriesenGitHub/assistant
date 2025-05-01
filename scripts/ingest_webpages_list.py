import logging

logging.getLogger("sqlalchemy.engine.Engine").disabled = True

from ingestion.tasks.ingest_webpages_list_task import ingest_webpages_list

if __name__ == "__main__":
    ingest_webpages_list.run()
