from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv
import os
import json

# Load .env
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
print("CONFIG:", CONFIG)

# Init Clients
blob_service = BlobServiceClient.from_connection_string(CONFIG["BLOB"]["CONNECTION_STRING"])
blob_container = blob_service.get_container_client(CONFIG["BLOB"]["CONTAINER"])

cosmos_client = CosmosClient(CONFIG["COSMOS"]["URI"], credential=CONFIG["COSMOS"]["KEY"])
cosmos_container = cosmos_client.get_database_client(CONFIG["COSMOS"]["DB"]).get_container_client(CONFIG["COSMOS"]["CONTAINER"])

# Loop through all blobs
blobs = blob_container.list_blobs()
restored_count = 0

for blob in blobs:
    print(f"📄 Reading Blob: {blob.name}")
    blob_data = blob_container.download_blob(blob.name).readall()
    try:
        records = json.loads(blob_data)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse {blob.name}: {e}")
        continue

    # Ensure the blob is a list (from archive script)
    if not isinstance(records, list):
        print(f"⚠️ Skipping blob with unexpected format: {blob.name}")
        continue

    for record in records:
        if not isinstance(record, dict):
            print(f"⚠️ Skipping non-dictionary record: {record}")
            continue
        if not record.get("id") or not record.get("userId"):
            print(f"⚠️ Skipping invalid record: {record}")
            continue
        try:
            cosmos_container.upsert_item(record)
            print(f"✅ Restored: {record['id']}")
            restored_count += 1
        except Exception as e:
            print(f"❌ Failed to insert record {record.get('id', '[no-id]')}: {e}")

print(f"\n🎉 Total records restored: {restored_count}")
