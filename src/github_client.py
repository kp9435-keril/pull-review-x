import json
import requests
from src.constants import *
from src.exceptions import GitHubAPIException, InvalidGitHubConfigException
from src.helpers import EnvironmentVariableHelper


class GitHubClient:
    def __init__(self):
        self.token = EnvironmentVariableHelper.get_github_auth_token()
        if self.token is None:
            raise InvalidGitHubConfigException("GitHub Token is required for GitHub's REST APIs")
        
        self.repository_link = EnvironmentVariableHelper.get_repo()
        if self.repository_link is None:
            raise InvalidGitHubConfigException("Repository is required for GitHub's REST APIs")
        
        self.owner, self.repo = self.repository_link.split("/")
        if self.owner is None or self.repo is None:
            raise InvalidGitHubConfigException("Error in parsing repository link, expected format: owner/repo")

        self.pr_number = EnvironmentVariableHelper.get_pr_number()
        if self.pr_number is None:
            raise InvalidGitHubConfigException("PR number is required for GitHub's REST APIs")
        
        self.pr_event = EnvironmentVariableHelper.get_event()
        if self.pr_event is None:
            raise InvalidGitHubConfigException("PR event is required for GitHub's REST APIs")

    def get_pr_info(self):
        """
        get https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}
        :return:
        """       
        headers = {
            "Accept": "application/vnd.github+json",
            "authorization": f"Bearer {self.token}",
        }

        pr_comments_url = PR_INFO_URL_TEMPLATE.format(self.owner, self.repo, self.pr_number)

        try:
            response = requests.get(pr_comments_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            raise GitHubAPIException(f"Error in get_pr_info: {err}")
    
    def get_pr_diff_files(self):
        """
        get https://api.github.com/repos/{owner}/{repo}/compare/{base}...{head}
        :return: 
        """
        try:
            pr_event = json.loads(self.pr_event)
            pr_request = pr_event["pull_request"]
            base_sha = pr_request["base"]["sha"]
            head_sha = pr_request["head"]["sha"]
        except Exception as err:
            raise GitHubAPIException(f"Error in parsing PR event: {err}")

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
        
    def post_pr_comment(self, comment: str):
        """
        post https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments
        :param comment:
        :return:
        """
        headers = {
            "Accept": "application/vnd.github+json",
            "authorization": f"Bearer {self.token}",
        }
        pr_comment_url = PR_COMMENT_URL_TEMPLATE.format(self.owner, self.repo, self.pr_number)
        data = {
            "body": comment
        }
        try:
            response = requests.post(pr_comment_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            return response.json()
        except Exception as err:
            raise GitHubAPIException(f"Error in post_pr_comment: {err}")
        
    def get_file_contents(self, contents_url: str):
        """
        get contents_url
        :param contents_url:
        :return:
        """
        headers = {
            "Accept": "application/vnd.github.raw+json",
            "authorization": f"Bearer {self.token}",
        }
        try:
            response = requests.get(contents_url, headers=headers)
            response.raise_for_status()
            return response.text
        except Exception as err:
            raise GitHubAPIException(f"Error in get_file_contents: {err}")
    
    def post_review_comment(self, comment: dict[str, str]):
        """
        post https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/comments
        :param comment:
        :return:
        """
        headers = {
            "Accept": "application/vnd.github+json",
            "authorization": f"Bearer {self.token}",
        }
        pr_review_url = PR_REVIEW_COMMENT_URL_TEMPLATE.format(self.owner, self.repo, self.pr_number)
        try:
            response = requests.post(pr_review_url, headers=headers, data=json.dumps(comment))
            response.raise_for_status()
            return response.json()
        except Exception as err:
            raise GitHubAPIException(f"Error in post_review_comment: {err}")