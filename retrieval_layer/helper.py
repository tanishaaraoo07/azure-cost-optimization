import os
import json
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "COSMOS": {
        "URI": os.getenv("COSMOS_URI"),
        "KEY": os.getenv("COSMOS_KEY"),
        "DB": os.getenv("COSMOS_DB_NAME"),
        "CONTAINER": os.getenv("COSMOS_CONTAINER_NAME")
    },
    "BLOB": {
        "CONNECTION_STRING": os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
        "CONTAINER": os.getenv("BLOB_CONTAINER_NAME")
    }
}

def fetch_data(source='cosmos'):
    if source == 'cosmos':
        cosmos = CosmosClient(CONFIG["COSMOS"]["URI"], credential=CONFIG["COSMOS"]["KEY"])
        container = cosmos.get_database_client(CONFIG["COSMOS"]["DB"]).get_container_client(CONFIG["COSMOS"]["CONTAINER"])
        query = "SELECT * FROM c"
        return list(container.query_items(query=query, enable_cross_partition_query=True))

    elif source == 'archive':
        blob_service = BlobServiceClient.from_connection_string(CONFIG["BLOB"]["CONNECTION_STRING"])
        blob_container = blob_service.get_container_client(CONFIG["BLOB"]["CONTAINER"])
        blobs = blob_container.list_blobs()
        all_records = []
        for blob in blobs:
            blob_data = blob_container.download_blob(blob.name).readall()
            records = json.loads(blob_data)
            all_records.extend(records)
        return all_records

    else:
        raise ValueError("Invalid source specified. Use 'cosmos' or 'archive'.")
