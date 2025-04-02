import json
import logging
from typing import Optional

from openai import AzureOpenAI
from src.constants import *
from src.exceptions import InvalidOpenAIConfigException
from src.helpers import EnvironmentVariableHelper

logger = logging.getLogger(__name__)

class AzureOpenAIClient:
    def __init__(self):
        self.api_key = EnvironmentVariableHelper.get_azure_openai_apikey()
        self.endpoint = EnvironmentVariableHelper.get_azure_openai_endpoint()
        self.api_version = EnvironmentVariableHelper.get_azure_openai_api_version()
        self.model = EnvironmentVariableHelper.get_azure_openai_model()
        if not self.api_key or not self.endpoint or not self.api_version or not self.model:
            raise InvalidOpenAIConfigException("Invalid Azure OpenAI configuration. Please check the environment variables.")
        self.azure_openai_client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=self.api_version,
        )
    
    def request_gpt(self, messages: list[dict[str, str]]) -> Optional[str]:
        """
        request gpts with constructed messages
        :param messages: messages for gpt review
        :return:
          review_content: str, the review response
        """
        gpt_result = self.azure_openai_client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        content = json.loads(gpt_result.to_json())
        if "choices" not in content or not content["choices"]:
            return None
        review_message = content["choices"][0]["message"]["content"]
        return str(review_message)