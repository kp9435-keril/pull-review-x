import os

from openai import AzureOpenAI
from src.exceptions import InvalidOpenAIConfigException
from src.helpers import EnvironmentVariableHelper


class AzureOpenAIClient:
    def __init__(self):
        self.api_key = EnvironmentVariableHelper.get_azure_openai_apikey()
        self.endpoint = EnvironmentVariableHelper.get_azure_openai_endpoint()
        self.model = EnvironmentVariableHelper.get_azure_openai_model()
        self.model_api_version = EnvironmentVariableHelper.get_azure_openai_model_api_version()
        if not self.model or not self.model_api_version or not self.endpoint or not self.api_key:
            raise InvalidOpenAIConfigException("Azure OpenAI model, model API version, endpoint and API key are required")
        self.azure_openai_client = AzureOpenAI(
            api_version=self.model_api_version,
            api_key=self.api_key,
            azure_endpoint=self.endpoint
        )