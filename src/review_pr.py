import json
import logging
from typing import Any
from src.azure_openai_client import AzureOpenAIClient
from src.github_client import GitHubClient
from src.helpers import EnvironmentVariableHelper
from src.utils import *

logger = logging.getLogger(__name__)

class ReviewPR:
    def __init__(self):
        self.github_client = GitHubClient()
        self.azure_openai_client = AzureOpenAIClient()
    
    def review_pr(self):
        pr_diffs = self.github_client.get_pr_diff_files()

        get_pr_summary = EnvironmentVariableHelper.get_pr_summary()
        if get_pr_summary:
            self.get_pr_summary(pr_diffs=pr_diffs)
    
    def get_pr_summary(self, pr_diffs: dict[str, Any]) -> None:
        if not pr_diffs or "files" not in pr_diffs or not pr_diffs["files"]:
            logger.warning("No pr diff files, pr summary ignored")
            return
        pr_content_patches = [diff_item["patch"] for diff_item in pr_diffs["files"] if diff_item["filename"].find("/tests/") == -1]
        commit_messages = [commit["commit"]["message"] for commit in pr_diffs["commits"]]
        logger.warning(pr_content_patches)
        logger.warning(commit_messages)
        # messages: list[dict[str, str]] = []
        # format_gpt_message(messages, [PR_SUMMARY_PROMPT], role=MODEL_USER_ROLE)
        # format_gpt_message(messages, ["\n".join(pr_content_patches)], role=MODEL_USER_ROLE)
        # logger.warning(messages)
        # gpt_resp = self.azure_openai_client.request_gpt(messages)
        # if not gpt_resp:
        #     return