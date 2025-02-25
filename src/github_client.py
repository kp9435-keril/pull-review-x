import os

from src.exceptions import *


class GitHubClient:
    def __init__(self):
        self.token = os.environ.get("GITHUB_AUTH_TOKEN", None)
        if not self.token:
            raise GitTokenMissingException("GitHub Token is required for REST APIs")
        self.repositoryLink = os.environ.get("REPO", None)
        if not self.repositoryLink:
            raise RepoMissingException("Repository is required for REST APIs")
        self.owner, self.repo = self.repositoryLink.split("/")
