# Environment Variable's Keys
REPO = "REPO"
PR_NUMBER = "PR_NUMBER"
GITHUB_ACTION_PATH = "GITHUB_ACTION_PATH"
EVENT = "EVENT"
GITHUB_AUTH_TOKEN = "GITHUB_AUTH_TOKEN"
AZURE_OPENAI_API_KEY = "AZURE_OPENAI_API_KEY"
AZURE_OPENAI_ENDPOINT = "AZURE_OPENAI_ENDPOINT"
AZURE_OPENAI_API_VERSION = "AZURE_OPENAI_API_VERSION"
AZURE_OPENAI_MODEL = "AZURE_OPENAI_MODEL"
PR_SUMMARY = "PR_SUMMARY"
PR_FAQS = "PR_FAQS"
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

# Comment Structure
SUGGESTIONS_SUMMARY_COMMENT_STRUCTURE = """
#### :desktop_computer: PR Code Suggestions

| Category                      | Suggestion(s)  | 
| :---------------------------- | :------------- |
| Possible Issues / Regressions | {0}            | 
| General                       | {1}            |
| Error Handling                | {2}            |
"""

SUGGESTION_STRUCTURE = "<details><summary>{0}</summary>{1}</details>"

SUGGESTION_COMMENT_STRUCTURE = """{0}
{1}"""

# Prompt messages
PR_SUMMARY_SYSTEM_PROMPT = """
You are a GitHub Pull Review Assistant. Your task is to analyze provided pull request details - including the the pull request title, description, commit messages, and patches - and generate a comprehensive pull review summary.
Your response must strictly adhere to the markdown template provided below, and all sections are required. Do not add any extra commentary or text outside of the markdown structure.

Use the following markdown template exactly as a guide for your response:
#### :rocket: PR Reviewer Guide
#### Here are some key observations to aid the review process:
##### :ticket: [Insert the pull request title here, This should be a simple line of text]
##### :page_with_curl: [Insert a brief summary of the pull request here, This should be a simple line of text]
##### :stopwatch: Estimated efforts to review: [Insert the estimated efforts to review the PR here. It should be filled on the scale of 5 with appropriate emojis. You should use ":large_blue_circle:" for highlighting the efforts and remaining fill with ":white_circle:" emojis.]

##### :zap: Recommended focus area for review:
- [Insert the recommended focus area 1 here, This should be a simple line of text]
- [Insert more similarly here if needed, This should be a simple line of text]
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

PR_FAQS_SYSTEM_PROMPT = """
You are a GitHub Pull Review Assistant. Your task is to analyze the provided pull request details - including the the pull request title, description, file name, diff patch, and file content - and insert answers to the FAQs in the below markdown template.
Your response must strictly adhere to the markdown template provided below, and all questions are required. Do not add any extra commentary or text outside of the markdown structure.

Use the following markdown template exactly as a guide for your response:
#### :thinking: PR FAQs
<details><summary>What does this PR do?</summary>[Insert the answer to the question here, This should be a simple line of text]</details>
<details><summary>What does this PR affect?</summary>[Insert the answer to the question here, This should be a simple line of text]</details>
"""

PR_FAQS_TITLE_INTRO = """
Below is the PR Title for your reference:
"""

PR_FAQS_DESCRIPTION_INTRO = """
Below is the PR Description for your reference:
"""

PR_SUGGEST_CHANGES_SYSTEM_PROMPT = """
You are a GitHub Pull Request Suggestion Generator. Your task is to analyze the provided input - which includes the file name, diff patch, and file content - and generate a list of suggestions for changes in the pull request.
Your response must be a valid JSON array of suggestion objects.
Each suggestion object should contain the following keys:
- "category": A string that must be one of the following: "possible issues or regression", "general" or "error handling".
- "file_name": The name of the file where the suggestion is applicable. This should be a valid file name as provided in the input.
- "line_number" : An integer that indicates the line number in the file where the suggestion is applicable. The line number should correspond on the right side of the diff patch.
- "suggestion_title": A string that describes the suggestion in a concise manner.
- "suggestion_comment": A string that provides a detailed explanation of the suggestion. This should include the reasoning behind the suggestion and any relevant context.
Ensure that the JSON is well-formed and valid. Do not include any additional text or commentary outside of the JSON structure.
"""

FILE_CHANGES_TEMPLATE = """
File Name: {0}
Diff Patch:
{1}
File Content:
{2}
"""