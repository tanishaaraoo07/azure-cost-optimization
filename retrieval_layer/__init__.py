import logging
import azure.functions as func
from .helper import fetch_data
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    source = req.params.get('source', 'cosmos')
    try:
        data = fetch_data(source)
        return func.HttpResponse(body=json.dumps(data), status_code=200, mimetype="application/json")
    except ValueError as ve:
        return func.HttpResponse(str(ve), status_code=400)
    except Exception as e:
        logging.exception("❌ Error fetching data")
        return func.HttpResponse("Internal Server Error", status_code=500)
