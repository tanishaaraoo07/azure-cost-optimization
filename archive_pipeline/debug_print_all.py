import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from azure.cosmos import CosmosClient
from utils.config import CONFIG

client = CosmosClient(CONFIG["COSMOS"]["URI"], CONFIG["COSMOS"]["KEY"])
database = client.get_database_client(CONFIG["COSMOS"]["DB"])
container = database.get_container_client(CONFIG["COSMOS"]["CONTAINER"])

items = list(container.read_all_items())
print(f"\n🔍 Found {len(items)} records:\n")

for item in items:
    print(item)
