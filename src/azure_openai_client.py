import json
from typing import Optional
from openai import AzureOpenAI
from src.exceptions import InvalidOpenAIConfigException, OpenAIAPIException
from src.helpers import EnvironmentVariableHelper


class AzureOpenAIClient:
    def __init__(self):
        self.api_key = EnvironmentVariableHelper.get_azure_openai_apikey()
        if self.api_key is None:
            raise InvalidOpenAIConfigException("Azure OpenAI API key is not set.")
        
        self.endpoint = EnvironmentVariableHelper.get_azure_openai_endpoint()
        if self.endpoint is None:
            raise InvalidOpenAIConfigException("Azure OpenAI endpoint is not set.")
        
        self.api_version = EnvironmentVariableHelper.get_azure_openai_api_version()
        if self.api_version is None:
            raise InvalidOpenAIConfigException("Azure OpenAI API version is not set.")
        
        self.model = EnvironmentVariableHelper.get_azure_openai_model()
        if self.model is None:
            raise InvalidOpenAIConfigException("Azure OpenAI model is not set.")
            
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
        try:
            gpt_result = self.azure_openai_client.chat.completions.create(
            model=self.model,
            messages=messages
            )
            content = json.loads(gpt_result.to_json())
            if "choices" not in content or not content["choices"]:
                return None
            review_message = content["choices"][0]["message"]["content"]
            return str(review_message)
        except Exception as err:
            raise OpenAIAPIException(f"Error in request_gpt: {err}")