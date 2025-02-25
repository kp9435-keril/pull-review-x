OPENAI_API_VERSION = "2025-01-01-preview"

# Environment Variable's Keys
GITHUB_AUTH_TOKEN = "GITHUB_AUTH_TOKEN"
REPO = "REPO"
EVENT = "EVENT"
AZURE_OPENAI_APIKEY = "AZURE_OPENAI_APIKEY"
AZURE_OPENAI_ENDPOINT = "AZURE_OPENAI_ENDPOINT"
AZURE_OPENAI_MODEL = "AZURE_OPENAI_MODEL"
PR_SUMMARY = "PR_SUMMARY"
PR_SUGGEST_CHANGES = "PR_SUGGEST_CHANGES"

# GitHub API URL
PR_COMMENTS_URL_TEMPLATE = "https://api.github.com/repos/{0}/{1}/pulls/{2}/comments"
PR_DIFF_URL_TEMPLATE = "https://api.github.com/repos/{0}/{1}/compare/{2}...{3}"

# Model Roles
MODEL_SYSTEM_ROLE = "system"
MODEL_USER_ROLE = "user"
MODEL_ASSIST_ROLE = "assistant"

# Prompt messages

PR_SUMMARY_PROMPT = """
Below is the whole changed content from a github pull requests, please draw a summary of this pr with no more than 100 words. Ignore the history notes updates. 
And please use the following format:
PR Summary:
1. balabala
2. balabala
...
"""

PR_TAG = """
:mag_right:
"""

PR_EVALUATE_PROMPT = """
Below is a list of evaluation score for existing git pr review result and its corresponding score, delimitd by @@@.
Nothing to return.@@@-10
The URL is incomplete. It should be https://learn.microsoft.com/en-us/cli/azure/monitor/data-collection/endpoint/association?view=azure-cli-latest#az-monitor-data-collection-endpoint-association-list.@@@5
The placeholder <resource/monitor/endpoint_id> should be enclosed in backticks for clarity and compliance with markdown formatting.@@@3
`az aks connection create` should be backticked in the history notes for consistency with the previous usage.@@@-1
Review-Ignored@@@-10
Can you evaluate the below sentence according to the standard set up in the above evaluation example data list, just give a score please:

"""
