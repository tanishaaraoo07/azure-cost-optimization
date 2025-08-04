import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from azure.cosmos import CosmosClient
from utils.config import CONFIG
from datetime import datetime, timedelta
import uuid

# Cosmos setup
client = CosmosClient(CONFIG["COSMOS"]["URI"], CONFIG["COSMOS"]["KEY"])
database = client.get_database_client(CONFIG["COSMOS"]["DB"])
container = database.get_container_client(CONFIG["COSMOS"]["CONTAINER"])

# Insert a record older than 3 months
old_timestamp = (datetime.utcnow() - timedelta(days=100)).isoformat()

item = {
    "id": str(uuid.uuid4()),
    "name": "Sample Record",
    "timestamp": old_timestamp,
    "type": "log",
    "userId": "demo-user-123",  # ✅ Required for partition key
    "data": {
        "message": "Old log entry to be archived"
    }
}

container.create_item(body=item)
print(f"✅ Inserted old record: {item['id']}")
