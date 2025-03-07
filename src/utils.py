import logging
import re
from typing import Any
from src.constants import *

logger = logging.getLogger(__name__)

def format_gpt_message(messages: list[dict[str, str]], contents: list[str], role: str = MODEL_USER_ROLE) -> None:
    """
    fill request messages
    :param messages: messages altered for gpt review
    :param role: message role
    :param contents: message to be reviewed
    :return: None
    """
    for content in contents:
        messages.append({
            "role": role,
            "content": content
        })

def generate_changes_suggestion_comment(table_data: dict[str, Any]) -> str:
    """
    generate html table from table data
    :param table_data: table data
    :return: html table
    """
    comment = f"""
#### :desktop_computer: PR Code Suggestions"""

    comment += f"""
| Category                      | Suggestion(s)                                                                  | 
| :---------------------------- | :----------------------------------------------------------------------------- |
| Possible Issues / Regressions | {generate_suggestions_cell_data(table_data["possible_issues_or_regressions"])} |
| General                       | {generate_suggestions_cell_data(table_data["general"])}                        |
| Error Handling                | {generate_suggestions_cell_data(table_data["error_handling"])}                 |
"""
    return comment

def generate_suggestions_cell_data(suggestions: list[dict[str, str]]) -> str:
    """
    generate suggestions cell data
    :param suggestions: suggestions
    :return: suggestions cell data
    """
    if not suggestions:
        return "Looks like this came up clean! :fire:"
    suggestions_data = ""
    for suggestion in suggestions:
        suggestions_data += f"<details><summary>{suggestion["suggestion_title"]}</summary>{suggestion['suggestion_comment']}</details>"
    return suggestions_data

def get_comment_body(suggestion_title: str, suggestion_comment: str) -> str:
    """
    get comment body
    :param suggestion_title: suggestion title
    :param suggestion_comment: suggestion comment
    :return: comment body
    """
    return f"""{suggestion_title}
{suggestion_comment}""";

GIT_PATCH_PATTERN = r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@'


def filter_review_patch_pattern(patch_body: str) -> bool:
    matches = re.findall(GIT_PATCH_PATTERN, patch_body)
    return len(matches) != 1


def get_patch_position(patch_body: str) -> int:
    match = re.match(GIT_PATCH_PATTERN, patch_body)
    if match:
        old_start, old_length, new_start, new_length = match.groups()
    else:
        logger.warning("No git patch found, shouldn't be here")
        return 1
    start: int = int(new_start)
    last_add: int = 0
    line_add: int = 0
    for line in patch_body.split("\n"):
        if line.find("-") == 0:
            continue
        line_add += 1
        if line.find("+") == 0:
            last_add = line_add
    return start + last_add - 2