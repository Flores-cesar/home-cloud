import azure.functions as func
import logging
from app.api.health import health_check
from app.api.echo import echo_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

# ============================================================================
# CUSTOM API ENDPOINTS
# ============================================================================

@app.route(route="health", methods=["GET"])
async def health_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint"""
    logger.info("Health endpoint called")
    return await health_check(req)


@app.route(route="echo", methods=["POST"])
async def echo_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """Echo endpoint that processes JSON data"""
    logger.info("Echo endpoint called")
    return await echo_data(req)