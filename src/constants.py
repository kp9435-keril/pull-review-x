OPENAI_API_VERSION = "2025-01-01-preview"

# Environment Variable's Keys
REPO = "REPO"
PR_NUMBER = "PR_NUMBER"
GITHUB_ACTION_PATH = "GITHUB_ACTION_PATH"
EVENT = "EVENT"
GITHUB_AUTH_TOKEN = "GITHUB_AUTH_TOKEN"
AZURE_OPENAI_APIKEY = "AZURE_OPENAI_APIKEY"
AZURE_OPENAI_ENDPOINT = "AZURE_OPENAI_ENDPOINT"
AZURE_OPENAI_MODEL = "AZURE_OPENAI_MODEL"
PR_SUMMARY = "PR_SUMMARY"
PR_SUGGEST_CHANGES = "PR_SUGGEST_CHANGES"

# GitHub API URL
PR_INFO_URL_TEMPLATE = "https://api.github.com/repos/{0}/{1}/pulls/{2}"
PR_COMMENTS_URL_TEMPLATE = "https://api.github.com/repos/{0}/{1}/pulls/{2}/comments"
PR_DIFF_URL_TEMPLATE = "https://api.github.com/repos/{0}/{1}/compare/{2}...{3}"

# Model Roles
MODEL_SYSTEM_ROLE = "system"
MODEL_USER_ROLE = "user"
MODEL_ASSIST_ROLE = "assistant"

# Prompt messages

PR_SUMMARY_SYSTEM_PROMPT = """
You are a highly intelligent AI assistant designed to generate comprehensive, structured, and insightful pull request (PR) review summaries.
Your primary objective is to analyze PR Description, PR Title, PR Commits, and PR Changes to generate a concise and informative summary.

Please adhere to the following guidelines:
1. Be Objective & Informative.
2. Maintain a Constructive & Professional Tone.
3. Ensure Markdown Formatting.
4. Follow a proper summary structure.

The summary should be point-wise and cover the following aspects:
1. PR Description Summary.
2. PR Title Analysis.
3. PR Commits Overview.
4. PR Changes Analysis.

Feel free to use professional emojis to enhance the summary.
"""

PR_SUMMARY_COMMIT_MESSAGES_INTRO = """
Below are the list of commit messages in the PR for your reference:

"""

PR_SUMMARY_PATCHES_INTRO = """
Below are the list of file changes in the PR for your reference:

"""