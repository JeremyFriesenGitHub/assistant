from ingestion.tasks.ingest_webpages_list_task import ingest_webpages_list

if __name__ == "__main__":
    result = ingest_webpages_list.delay()
    print(f"Task ID: {result.id}")
