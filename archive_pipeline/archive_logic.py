import os
import json
from datetime import datetime, timedelta
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

def archive_old_cosmos_records():
    # Cosmos DB client setup
    cosmos = CosmosClient(CONFIG["COSMOS"]["URI"], credential=CONFIG["COSMOS"]["KEY"])
    container = cosmos.get_database_client(CONFIG["COSMOS"]["DB"]).get_container_client(CONFIG["COSMOS"]["CONTAINER"])

    # Blob storage setup
    blob_service = BlobServiceClient.from_connection_string(CONFIG["BLOB"]["CONNECTION_STRING"])
    blob_container = blob_service.get_container_client(CONFIG["BLOB"]["CONTAINER"])

    # Defensive container creation
    try:
        if not blob_container.exists():
            blob_container.create_container()
    except Exception as e:
        print(f"[ERROR] Failed to verify/create blob container: {e}")
        return 0

    # Calculate threshold date for archival (90 days ago)
    threshold_date = (datetime.utcnow() - timedelta(days=90)).isoformat()

    # Query old documents
    query = f"SELECT * FROM c WHERE c.timestamp < '{threshold_date}'"
    results = list(container.query_items(query=query, enable_cross_partition_query=True))

    if not results:
        print("[INFO] No records found older than 90 days.")
        return 0

    # Archive to blob
    blob_name = f"archived_{datetime.utcnow().isoformat()}.json"
    try:
        blob_container.upload_blob(name=blob_name, data=json.dumps(results), overwrite=True)
        print(f"[INFO] Archived {len(results)} records to blob: {blob_name}")
    except Exception as e:
        print(f"[ERROR] Failed to upload archive to blob: {e}")
        return 0

    # Delete archived items from Cosmos DB
    deleted_count = 0
    for doc in results:
        user_id = doc.get("userId")
        if user_id:
            try:
                container.delete_item(item=doc["id"], partition_key=user_id)
                deleted_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to delete doc {doc['id']}: {e}")
        else:
            print(f"[WARNING] Skipping doc {doc.get('id')} - missing userId (partition key)")

    print(f"[INFO] Deleted {deleted_count} records from Cosmos DB.")
    return deleted_count
