import os

from openai import AzureOpenAI
from src.exceptions import InvalidOpenAIConfigException


class AzureOpenAIClient:
    def __init__(self):
        self.model = os.environ.get("AZURE_OPENAI_MODEL", None)
        self.model_api_version = os.environ.get("AZURE_OPENAI_MODEL_API_VERSION", None)
        self.endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", None)
        self.api_key = os.environ.get("AZURE_OPENAI_API_KEY", None)
        if not self.model or not self.model_api_version or not self.endpoint or not self.api_key:
            raise InvalidOpenAIConfigException("Azure OpenAI model, model API version, endpoint and API key are required")
        self.azure_openai_client = AzureOpenAI(
            api_version=self.model_api_version,
            api_key=self.api_key,
            azure_endpoint=self.endpoint
        )