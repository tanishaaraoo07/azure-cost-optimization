# retrieve.py (example)
import os, json
from datetime import datetime, timedelta
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

cutoff = datetime.utcnow() - timedelta(days=90)
client = CosmosClient(os.getenv("COSMOS_URI"), os.getenv("COSMOS_KEY"))
cosmos_container = client.get_database_client(os.getenv("COSMOS_DB")).get_container_client(os.getenv("COSMOS_CONTAINER"))
blob_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING")).get_container_client(os.getenv("BLOB_CONTAINER_NAME"))

def get_record(record_id, record_date, partition_key=None):
    record_dt = datetime.fromisoformat(record_date)
    if record_dt >= cutoff:
        try:
            item = cosmos_container.read_item(item=record_id, partition_key=partition_key or record_id)
            return {"source": "cosmos", "data": item}
        except Exception:
            pass
    try:
        blob = blob_client.get_blob_client(f"{record_id}.json")
        content = blob.download_blob().readall()
        return {"source": "blob", "data": json.loads(content)}
    except Exception:
        return {"error": "Not found in both data stores"}
