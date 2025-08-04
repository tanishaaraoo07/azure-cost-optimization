from dotenv import load_dotenv
import os

load_dotenv()

CONFIG = {
    "COSMOS": {
        "URI": os.getenv("COSMOS_URI"),
        "KEY": os.getenv("COSMOS_KEY"),
        "DB": os.getenv("COSMOS_DB"),
        "CONTAINER": os.getenv("COSMOS_CONTAINER")
    },
    "BLOB": {
        "CONNECTION_STRING": os.getenv("AZURE_STORAGE_CONNECTION_STRING"),  # ✅ match .env
        "CONTAINER": os.getenv("BLOB_CONTAINER_NAME")  # ✅ match .env
    }
}
