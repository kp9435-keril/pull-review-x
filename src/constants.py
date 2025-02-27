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
PR_COMMENT_SUGGESTED_CHANGES = "PR_COMMENT_SUGGESTED_CHANGES"

# GitHub API URL
PR_INFO_URL_TEMPLATE = "https://api.github.com/repos/{0}/{1}/pulls/{2}"
PR_DIFF_URL_TEMPLATE = "https://api.github.com/repos/{0}/{1}/compare/{2}...{3}"
PR_COMMENT_URL_TEMPLATE = "https://api.github.com/repos/{0}/{1}/issues/{2}/comments"
PR_REVIEW_COMMENT_URL_TEMPLATE = "https://api.github.com/repos/{0}/{1}/pulls/{2}/comments"

# Model Roles
MODEL_SYSTEM_ROLE = "system"
MODEL_USER_ROLE = "user"
MODEL_ASSIST_ROLE = "assistant"

# Prompt messages

PR_SUMMARY_SYSTEM_PROMPT = """
You are a highly intelligent AI assistant designed to generate comprehensive, structured, and insightful pull request (PR) review summaries.
Your primary objective is to analyze PR Title, PR Description, PR Commit Messages, and PR Change Patches to generate a concise and informative summary.

The response should strictly in markdown format given below. 
The "Title summary goes here" and "Description Summary goes here" are placeholders for you to fill in with the appropriate content. Replace it with appropriate content.
The "Estimated efforts goes here" is a placeholder for you to fill in with the estimated efforts to review the PR. It should be filled on the scale of 5 with appropriate emojis. You should use ":large_blue_circle:" for highlighting the efforts and remaining fill with ":white_circle:" emojis.
The "Recommended focus area 1 goes here" section should be filled with the appropriate focus area. You can add more focus areas as needed. 

Please adhere strictly to the following markdown format for the PR summary:
#### :rocket: PR Reviewer Guide
#### Here are some key observations to aid the review process:
##### :ticket: "Title summary goes here"
##### :page_with_curl: "Description Summary goes here"
##### :stopwatch: Estimated efforts to review: "Estimated efforts goes here"

##### :zap: Recommended focus area for review
- "Recommended focus area 1 goes here"
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

PR_SUGGEST_CHANGES_SYSTEM_PROMPT = """
You are a highly intelligent AI assistant designed to generate comprehensive, structured, and insightful pull request (PR) review suggestions.
Your primary objective is to analyze PR Change Patches for issues in 3 categories "Possible Issues/Regressions", "General", "Error Handling" and provide suggestions.

Please note suggestions that should not repeat and are not similar across categories. Also, if there are multiple suggestions on same lines of patch, kindly club the suggestion into one.

Let's understand the keys of suggestion map object given below (all 4 fields are mandatory for a suggestion):
"filename" - The filename of the file where the changes are made, this should be same as provided in the input.
"diff_patch" - The diff patch of the file, this should be same as provided in the input.
"suggestion_title" - It should contain relevant title for the suggestion.
"suggestion_comment" - The comment of the suggestion should be crystal clear and concise. It should be text and only text.

Please adhere strictly to the following json format for your response:
{
    "possible_issues_or_regressions": [
        {
            "filename": "...",
            "diff_patch": "...",
            "suggestion_title": "...",
            "suggestion_comment": "..."
        }
    ],
    "general": [
        {
            "filename": "...",
            "diff_patch": "...",
            "suggestion_title": "...",
            "suggestion_comment": "..."
        }
    ],
    "error_handling": [
        {
            "filename": "...",
            "diff_patch": "...",
            "suggestion_title": "...",
            "suggestion_comment": "..."
        }
    ],
}
Please ensure that your response should always be a valid json object string and adhere to the above format.
"""

FILE_CHANGES_TEMPLATE = """
Filename: {0}
Diff Patch:
{1}
File Content:
{2}
"""