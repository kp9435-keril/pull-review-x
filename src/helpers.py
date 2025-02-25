import os
from typing import Any

from src.constants import *


class EnvironmentVariableHelper:
    @staticmethod
    def get_github_auth_token() -> str:
        return EnvironmentVariableHelper.get_env_var(GITHUB_AUTH_TOKEN, None)
    
    @staticmethod
    def get_repo() -> str:
        return EnvironmentVariableHelper.get_env_var(REPO, None)
    
    @staticmethod
    def get_event() -> str:
        return EnvironmentVariableHelper.get_env_var(EVENT, None)
    
    @staticmethod
    def get_azure_openai_apikey() -> str:
        return EnvironmentVariableHelper.get_env_var(AZURE_OPENAI_APIKEY, None)

    @staticmethod
    def get_azure_openai_endpoint() -> str:
        return EnvironmentVariableHelper.get_env_var(AZURE_OPENAI_ENDPOINT, None)
    
    @staticmethod
    def get_azure_openai_model() -> str:
        return EnvironmentVariableHelper.get_env_var(AZURE_OPENAI_MODEL, None)
    
    @staticmethod
    def get_azure_openai_model_api_version() -> str:
        return EnvironmentVariableHelper.get_env_var(AZURE_OPENAI_MODEL_API_VERSION, None)
    
    @staticmethod
    def get_pr_summary() -> bool:
        return EnvironmentVariableHelper.get_env_var(PR_SUMMARY, True)
    
    def get_pr_suggest_changes() -> bool:
        return EnvironmentVariableHelper.get_env_var(PR_SUGGEST_CHANGES, True)

    @staticmethod
    def get_env_var(name: str, fallback: Any) -> Any:
        return os.environ.get(name, fallback)