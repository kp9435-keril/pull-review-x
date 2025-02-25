import os

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
