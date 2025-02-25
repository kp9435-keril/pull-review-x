import json
import requests

from src.constants import *
from src.exceptions import *
from src.helpers import EnvironmentVariableHelper


class GitHubClient:
    def __init__(self):
        self.token = EnvironmentVariableHelper.get_github_auth_token()
        if not self.token:
            raise GitTokenMissingException("GitHub Token is required for REST APIs")
        self.repositoryLink = EnvironmentVariableHelper.get_repo()
        if not self.repositoryLink:
            raise RepoMissingException("Repository is required for REST APIs")
        self.owner, self.repo = self.repositoryLink.split("/")
    
    def get_pr_diff_files(self):
        """
        get https://api.github.com/repos/{owner}/{repo}/compare/{base}...{head}
        :return: 
        """
        raw_event = EnvironmentVariableHelper.get_event()
        if not raw_event:
            raise MissingConfigException("Please provide PR detail info")
        pr_event = json.loads(raw_event)
        pr_request = pr_event["pull_request"]
        base_sha = pr_request["base"]["sha"]
        head_sha = pr_request["head"]["sha"]
        headers = {
            "Accept": "application/vnd.github+json",
            "authorization": f"Bearer {self.token}",
        }

        pr_diff_url = PR_DIFF_URL_TEMPLATE.format(self.owner, self.repo, base_sha, head_sha)

        try:
            response = requests.get(pr_diff_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            raise GitHubAPIException(f"Error in get_pr_diff_files: {err}")
