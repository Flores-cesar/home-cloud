"""
Configuration settings for the Azure Function
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure Function Settings
FUNCTION_APP_NAME = os.getenv("FUNCTION_APP_NAME", "my-azure-function")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# API Settings
API_VERSION = "v1"
BASE_URL = f"/api/{API_VERSION}"

# Example: Azure Storage settings (uncomment when needed)
# AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
# AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "documents")

# Example: Azure Cognitive Services settings (uncomment when needed)
# AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
# AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")

# Example: Custom API settings
# CUSTOM_API_URL = os.getenv("CUSTOM_API_URL")
# CUSTOM_API_KEY = os.getenv("CUSTOM_API_KEY")