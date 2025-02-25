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
        pr_info = self.github_client.get_pr_info()

        get_pr_summary = EnvironmentVariableHelper.get_pr_summary()
        if get_pr_summary:
            self.get_pr_summary(pr_diffs=pr_diffs, pr_info=pr_info)
    
    def get_pr_summary(self, pr_diffs: dict[str, Any], pr_info: dict[str, Any]) -> None:
        if not pr_diffs or "files" not in pr_diffs or not pr_diffs["files"]:
            logger.warning("No pr diff files, pr summary ignored")
            return
        if not pr_diffs or "commits" not in pr_diffs or not pr_diffs["commits"]:
            logger.warning("No pr commits, pr summary ignored")
            return
        logger.warning(str(pr_diffs))
        pr_title = pr_info["title"] if "title" in pr_info else ""
        pr_description = pr_info["body"] if "body" in pr_info else ""
        pr_content_patches = [diff_item["patch"] for diff_item in pr_diffs["files"] if diff_item["filename"].find("/tests/") == -1]
        commit_messages = [commit["commit"]["message"] for commit in pr_diffs["commits"]]
        messages: list[dict[str, str]] = []
        format_gpt_message(messages, [PR_SUMMARY_SYSTEM_PROMPT], role=MODEL_SYSTEM_ROLE)
        format_gpt_message(messages, [PR_SUMMARY_TITLE_INTRO + pr_title], role=MODEL_USER_ROLE)
        format_gpt_message(messages, [PR_SUMMARY_DESCRIPTION_INTRO + pr_description], role=MODEL_USER_ROLE)
        format_gpt_message(messages, [PR_SUMMARY_COMMIT_MESSAGES_INTRO + "\n".join(commit_messages)], role=MODEL_USER_ROLE)
        format_gpt_message(messages, [PR_SUMMARY_PATCHES_INTRO + "\n".join(pr_content_patches)], role=MODEL_USER_ROLE)
        gpt_resp = self.azure_openai_client.request_gpt(messages)
        if not gpt_resp:
            return
        self.github_client.post_pr_comment(gpt_resp)
        return