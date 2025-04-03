from src.azure_openai_client import AzureOpenAIClient
from src.constants import *
from src.exceptions import GitHubAPIException, OpenAIAPIException
from src.github_client import GitHubClient
from src.helpers import EnvironmentVariableHelper
from src.utils import *


logger = logging.getLogger(__name__) 

class ReviewPR:
    def __init__(self):
        try :
            self.github_client = GitHubClient()
            self.azure_openai_client = AzureOpenAIClient()
        except Exception as err:
            logger.error("Error in initializing PullReviewX: %s", err)
            raise err

    def review_pr(self):
        try:
            pr_info = self.github_client.get_pr_info()
            pr_diffs = self.github_client.get_pr_diff_files()

            if not pr_diffs or "files" not in pr_diffs or not pr_diffs["files"]:
                logger.warning("No pr diff files, pr summary ignored")
                return
            if not pr_diffs or "commits" not in pr_diffs or not pr_diffs["commits"]:
                logger.warning("No pr commits, pr summary ignored")
                return

            pr_title = pr_info.get("title", "")
            pr_description = pr_info.get("body", "")
            commit_messages = [commit["commit"]["message"] for commit in pr_diffs["commits"]]
            pr_diff_contents = [diff_item for diff_item in pr_diffs["files"] if diff_item["filename"].find("/tests/") == -1]
            pr_last_commit_id = pr_diffs["commits"][-1]["sha"]

            get_pr_summary = EnvironmentVariableHelper.get_pr_summary()
            if get_pr_summary:
                self.get_pr_summary(pr_title=pr_title, pr_description=pr_description, commit_messages=commit_messages, pr_diff_contents=pr_diff_contents)

            get_pr_faqs = EnvironmentVariableHelper.get_pr_faqs()
            if get_pr_faqs:
                self.get_pr_faqs(pr_title=pr_title, pr_description=pr_description, pr_diff_contents=pr_diff_contents)
            
            get_pr_suggest_changes = EnvironmentVariableHelper.get_pr_suggest_changes()
            if get_pr_suggest_changes:
                self.get_pr_suggest_changes(pr_diff_contents=pr_diff_contents, pr_last_commit_id=pr_last_commit_id)
        
        except GitHubAPIException as err:
            logger.error("Error in review_pr, GitHub API error: %s", err)
            raise err

        except KeyError as err:
            logger.error("Error in review_pr, Key error: %s", err)
            raise err
        
        except Exception as err:
            logger.error("Unexpected Error in review_pr: %s", err)
            raise err


    def get_pr_summary(self, pr_title: str, pr_description: str, commit_messages: list[Any], pr_diff_contents: list[Any]) -> None:
        try:
            pr_content_patches = [diff_item["patch"] for diff_item in pr_diff_contents]
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
        
        except OpenAIAPIException as err:
            logger.error("Error in get_pr_summary, OpenAI API error: %s", err)
            raise err
        
        except GitHubAPIException as err:
            logger.error("Error in get_pr_summary, GitHub API error: %s", err)
            raise err

        except KeyError as err:
            logger.error("Error in get_pr_summary, Key error: %s", err)
            raise err
        
        except Exception as err:
            logger.error("Unexpected Error in get_pr_summary: %s", err)
            raise err
        
    def get_pr_faqs(self, pr_title: str, pr_description: str, pr_diff_contents: list[Any]) -> None:
        try:
            messages: list[dict[str, str]] = []

            format_gpt_message(messages, [PR_FAQS_SYSTEM_PROMPT], role=MODEL_SYSTEM_ROLE)
            format_gpt_message(messages, [PR_FAQS_TITLE_INTRO + pr_title], role=MODEL_USER_ROLE)
            format_gpt_message(messages, [PR_FAQS_DESCRIPTION_INTRO + pr_description], role=MODEL_USER_ROLE)

            for diff_item in pr_diff_contents:
                diff_filename = diff_item["filename"]
                diff_patch = diff_item["patch"]
                file_content = self.github_client.get_file_contents(diff_item["contents_url"])
                format_gpt_message(messages, [FILE_CHANGES_TEMPLATE.format(diff_filename, diff_patch, file_content)], role=MODEL_USER_ROLE)
            
            gpt_resp = self.azure_openai_client.request_gpt(messages)
            if not gpt_resp:
                return
            
            self.github_client.post_pr_comment(gpt_resp)
            return
        
        except OpenAIAPIException as err:
            logger.error("Error in get_pr_faqs, OpenAI API error: %s", err)
            raise err
        
        except GitHubAPIException as err:
            logger.error("Error in get_pr_faqs, GitHub API error: %s", err)
            raise err
        
        except KeyError as err:
            logger.error("Error in get_pr_faqs, Key error: %s", err)
            raise err
        
        except Exception as err:
            logger.error("Unexpected Error in get_pr_faqs: %s", err)
            raise err
    
    def get_pr_suggest_changes(self, pr_diff_contents: list[Any], pr_last_commit_id: str) -> None:
        try:
            messages: list[dict[str, str]] = []

            format_gpt_message(messages, [PR_SUGGEST_CHANGES_SYSTEM_PROMPT], role=MODEL_SYSTEM_ROLE)
            for diff_item in pr_diff_contents:
                diff_filename = diff_item["filename"]
                diff_patch = diff_item["patch"]
                file_content = self.github_client.get_file_contents(diff_item["contents_url"])
                format_gpt_message(messages, [FILE_CHANGES_TEMPLATE.format(diff_filename, diff_patch, file_content)], role=MODEL_USER_ROLE)
            
            gpt_resp = self.azure_openai_client.request_gpt(messages)
            if not gpt_resp:
                return
            
            suggestions = extract_suggestions_json_array(gpt_resp)
            categorized_suggestions = categorize_suggestions(suggestions)
            comment = generate_changes_suggestion_comment(categorized_suggestions)
            self.github_client.post_pr_comment(comment)

            get_pr_comment_suggested_changes = EnvironmentVariableHelper.get_pr_comment_suggested_changes()
            if get_pr_comment_suggested_changes:
                self.pr_comment_suggested_changes(pr_last_commit_id=pr_last_commit_id, categorized_suggestions=categorized_suggestions)

            return
        
        except OpenAIAPIException as err:
            logger.error("Error in get_pr_suggest_changes, OpenAI API error: %s", err)
            raise err
        
        except GitHubAPIException as err:
            logger.error("Error in get_pr_suggest_changes, GitHub API error: %s", err)
            raise err
        
        except KeyError as err:
            logger.error("Error in get_pr_suggest_changes, Key error: %s", err)
            raise err
        
        except Exception as err:
            logger.error("Unexpected Error in get_pr_suggest_changes: %s", err)
            raise err
    
    def pr_comment_suggested_changes(self, pr_last_commit_id: str, categorized_suggestions: dict[str, list[dict[str, str]]]) -> None:
        if not categorized_suggestions:
            logger.warning("No suggested changes, pr comment suggested changes ignored")
            return
        for _ , values in categorized_suggestions.items():
            for suggestion in values:
                try:
                    comment = {
                        "body": get_comment_body(suggestion["suggestion_title"], suggestion["suggestion_comment"]),
                        "commit_id": pr_last_commit_id,
                        "path": suggestion["file_name"],
                        "line": suggestion["line_number"],
                        "side": "RIGHT"
                    }
                    self.github_client.post_review_comment(comment)

                except GitHubAPIException as err:
                    logger.error("Error in pr_comment_suggested_changes, GitHub API error: %s", err)

                except KeyError as err:
                    logger.error("Error in pr_comment_suggested_changes, Key error: %s", err)
        return