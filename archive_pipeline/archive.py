import sys
import os
import base64
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")  # 🔧 Fix import path

import json
from datetime import datetime, timedelta
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
from utils.config import CONFIG

# Extract and clean Cosmos DB config
COSMOS_URI = CONFIG["COSMOS"]["URI"].strip()
COSMOS_KEY = CONFIG["COSMOS"]["KEY"].strip().rstrip(";")  # Remove any trailing semicolon

# 🔍 Debugging key
print("🔑 Cosmos URI:", COSMOS_URI)
print("🔑 Cosmos Key Length:", len(COSMOS_KEY))
print("🔑 Cosmos Key Ends With '=':", COSMOS_KEY.endswith("="))

# 🔒 Validate Base64 decoding manually (optional but helpful)
try:
    base64.b64decode(COSMOS_KEY)
    print("✅ Cosmos Key Base64 decode successful.")
except Exception as e:
    print("❌ Base64 decode error:", e)
    sys.exit(1)

# Cosmos DB setup
cosmos_client = CosmosClient(COSMOS_URI, COSMOS_KEY)
db = cosmos_client.get_database_client(CONFIG["COSMOS"]["DB"])
container = db.get_container_client(CONFIG["COSMOS"]["CONTAINER"])

# Azure Blob setup
blob_service = BlobServiceClient.from_connection_string(CONFIG["BLOB"]["CONNECTION_STRING"])
blob_container = blob_service.get_container_client(CONFIG["BLOB"]["CONTAINER"])

# Define cutoff date (older than 90 days)
cutoff_date = datetime.utcnow() - timedelta(days=90)
cutoff_iso = cutoff_date.isoformat()
print(f"📅 Archiving records older than: {cutoff_iso}")

# Query old records
query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff_iso}'"
items = list(container.query_items(query=query, enable_cross_partition_query=True))
print(f"🔎 Found {len(items)} old records to archive.")

# Archive and delete valid items
archived_items = []
for item in items:
    if "userId" not in item:
        print(f"⚠️  Skipping item without userId: {item['id']}")
        continue

    # Upload to blob
    archived_items.append(item)
    container.delete_item(item=item['id'], partition_key=item['userId'])
    print(f"🗑️  Deleted: {item['id']}")

# Save to blob if any archived
if archived_items:
    blob_name = f"archive-{datetime.utcnow().isoformat()}.json"
    blob_data = json.dumps(archived_items, indent=2)
    blob_container.upload_blob(blob_name, blob_data)
    print(f"💾 Archived {len(archived_items)} record(s) to Blob: {blob_name}")
else:
    print("📭 No valid records to archive.")
