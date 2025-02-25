import json
import logging
from typing import Optional

from openai import AzureOpenAI
from src.exceptions import InvalidOpenAIConfigException
from src.helpers import EnvironmentVariableHelper

logger = logging.getLogger(__name__)

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
        logger.info("gpt review message: {0}".format(review_message))
        return str(review_message)