import datetime
import logging
import azure.functions as func
from archive_pipeline.archive_logic import archive_old_cosmos_records


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().isoformat()
    logging.info(f"🔁 Archive function triggered at {utc_timestamp}")

    try:
        count = archive_old_records()
        logging.info(f"✅ Archived {count} record(s) to Blob Storage.")
    except Exception as e:
        logging.error(f"❌ Archival failed: {e}")
