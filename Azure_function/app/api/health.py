"""
Health check endpoint for the Azure Function
"""
import azure.functions as func
import logging
from datetime import datetime
from app.config.settings import ENVIRONMENT, FUNCTION_APP_NAME

logger = logging.getLogger(__name__)

async def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """
    Health check endpoint that returns system status
    """
    try:
        logger.info("Health check endpoint called")

        # Basic health information
        health_data = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "function_app": FUNCTION_APP_NAME,
            "environment": ENVIRONMENT,
            "version": "1.0.0"
        }

        return func.HttpResponse(
            body=str(health_data),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return func.HttpResponse(
            body='{"status": "unhealthy", "error": "' + str(e) + '"}',
            status_code=500,
            mimetype="application/json"
        )