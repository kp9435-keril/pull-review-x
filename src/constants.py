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
Your primary objective is to analyze PR Title, PR Description, PR Commit Messages, and PR Change Patches to generate a concise and informative summary.
The response should strictly in markdown format given below. 
The "Title summary goes here" and "Description Summary goes here" are placeholders you to fill in with the appropriate content.
The "Estimated efforts to review" section should be filled with the appropriate blue emoji based on the review efforts on the scale of 5 and remaining white emojis, take the given example as a reference.                     
The "Recommended focus area for review" section should be filled with the appropriate focus areas.

Please adhere strictly to the following markdown format for the PR summary:
#### :rocket:PR Reviewer Guide
#### Here are some key observations to aid the review process:
##### :ticket: Title summary goes here
##### :page_with_curl: Description Summary goes here
##### :stopwatch: Estimated efforts to review: :large_blue_circle: :large_blue_circle: :white_circle: :white_circle: :white_circle:

##### :zap: Recommended focus area for review
- First item
- Second item
- Third item
- Fourth item
"""

PR_SUMMARY_TITLE_INTRO = """
Below is the PR Title for your reference:
"""

PR_SUMMARY_DESCRIPTION_INTRO = """
Below is the PR Description for your reference:
"""

PR_SUMMARY_COMMIT_MESSAGES_INTRO = """
Below are the list of commit messages in the PR for your reference:
"""

PR_SUMMARY_PATCHES_INTRO = """
Below are the list of file changes in the PR for your reference:
"""