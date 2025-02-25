from src.azure_openai_client import AzureOpenAIClient
from src.github_client import GitHubClient


class ReviewPR:
    def __init__(self):
        self.github_client = GitHubClient()
        self.azure_openai_client = AzureOpenAIClient()