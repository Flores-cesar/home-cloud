"""
Echo endpoint that processes and returns JSON data
"""
import azure.functions as func
import json
import logging
from datetime import datetime
from app.config.settings import API_VERSION

logger = logging.getLogger(__name__)

async def echo_data(req: func.HttpRequest) -> func.HttpResponse:
    """
    Echo endpoint that receives JSON data and returns it with additional metadata
    """
    try:
        logger.info("Echo endpoint called")

        # Get request body
        req_body = req.get_json()

        # Add metadata
        response_data = {
            "api_version": API_VERSION,
            "echoed_data": req_body,
            "timestamp": datetime.utcnow().isoformat(),
            "method": req.method,
            "url": req.url
        }

        return func.HttpResponse(
            body=json.dumps(response_data, indent=2),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError as e:
        logger.error(f"Invalid JSON received: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({
                "error": "Invalid JSON format",
                "message": "Please send valid JSON in the request body"
            }),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logger.error(f"Echo endpoint failed: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({
                "error": "Internal server error",
                "message": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )