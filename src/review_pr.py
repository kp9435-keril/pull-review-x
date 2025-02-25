from typing import Any
from src.azure_openai_client import AzureOpenAIClient
from src.github_client import GitHubClient
from src.helpers import EnvironmentVariableHelper


class ReviewPR:
    def __init__(self):
        self.github_client = GitHubClient()
        self.azure_openai_client = AzureOpenAIClient()
    
    def review_pr(self):
        pr_diffs = self.git_manager.get_pr_diff_files()

        get_pr_summary = EnvironmentVariableHelper.get_pr_summary()
        if get_pr_summary:
            self.get_pr_summary(pr_diffs=pr_diffs)

        EnvironmentVariableHelper.get_pr_suggest_changes()
    
    def get_pr_summary(self, pr_diffs: dict[str, Any]) -> None:
        print("PR Summary")
        print(pr_diffs)