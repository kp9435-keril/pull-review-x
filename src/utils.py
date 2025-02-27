from typing import Any
from src.constants import *


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
| Category                      | Suggestion(s)                                                   | 
| :---------------------------- | :-------------------------------------------------------------- |
| Possible Issues / Regressions | {generate_suggestions_cell_data(table_data["possible_issues"])} |
| General                       | {generate_suggestions_cell_data(table_data["general"])}         |
| Error Handling                | {generate_suggestions_cell_data(table_data["error_handling"])}  |
| Best Practice                 | {generate_suggestions_cell_data(table_data["best_practice"])}   |
"""
    return comment

def generate_suggestions_cell_data(suggestions: list[dict[str, str]]) -> str:
    """
    generate suggestions cell data
    :param suggestions: suggestions
    :return: suggestions cell data
    """
    if not suggestions:
        return ":fire: Looks like this came up clean! :fire:"
    suggestions_data = ""
    for suggestion in suggestions:
        suggestions_data += f"<details><summary>{suggestion["suggestion_title"]}</summary>{suggestion['suggestion_description']}</details>"
    return suggestions_data
