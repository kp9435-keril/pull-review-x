from collections import defaultdict
import json
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
    try:
        for content in contents:
            messages.append({
                "role": role,
                "content": content
            })
    except Exception as err:
        raise Exception(f"Error in format_gpt_message: {err}")

def extract_suggestions_json_array(input_text: str) -> list[dict[str, Any]]:
    """
    extract json array from input text
    """
    try:
        pattern = r'\[\s*{.*?}\s*\]'
    
        match = re.search(pattern, input_text, re.DOTALL)

        if match:
            json_array_str = match.group(0)
            try:
                return json.loads(json_array_str)
            except json.JSONDecodeError:
                return []
    except Exception as err:
        raise Exception(f"Error in extract_suggestions_json_array: {err}")
    
def categorize_suggestions(suggestions: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """
    categorize suggestions into different categories
    """
    try:
        categorized_suggestions = defaultdict(list)
    
        for suggestion in suggestions:
            category = suggestion.get('category', 'uncategorized')
            categorized_suggestions[category].append(suggestion)
        
        return dict(categorized_suggestions)
    except Exception as err:
        raise Exception(f"Error in categorize_suggestions: {err}")

def generate_changes_suggestion_comment(table_data: dict[str, list[dict[str, Any]]]) -> str:
    """
    generate html table from table data
    :param table_data: table data
    :return: html table
    """
    try: 
        comment = SUGGESTIONS_SUMMARY_COMMENT_STRUCTURE.format(
            generate_suggestions_cell_data([] if not table_data.get("possible issues or regression") else table_data["possible issues or regression"]),
            generate_suggestions_cell_data([] if not table_data.get("general") else table_data["general"]),
            generate_suggestions_cell_data([] if not table_data.get("error handling") else table_data["error handling"]),
        )
        return comment
    except Exception as err:
        raise Exception(f"Error in generate_changes_suggestion_comment: {err}")

def generate_suggestions_cell_data(suggestions: list[dict[str, Any]]) -> str:
    """
    generate suggestions cell data
    :param suggestions: suggestions
    :return: suggestions cell data
    """
    try:
        if not suggestions:
            return "Looks like this came up clean! :fire:"
        
        suggestions_data = ""
        for suggestion in suggestions:
            try:
                suggestions_data += SUGGESTION_STRUCTURE.format(
                    suggestion["suggestion_title"],
                    suggestion["suggestion_comment"]
                )
            except KeyError as err:
                logger.warning(f"Warning in generate_suggestions_cell_data, Missing key: {err}")
                continue
        
        if not suggestions_data:
            return "Looks like this came up clean! :fire:"
        
        return suggestions_data
    except Exception as err:
        raise Exception(f"Error in generate_suggestions_cell_data: {err}")

def get_comment_body(suggestion_title: str, suggestion_comment: str) -> str:
    """
    get comment body
    :param suggestion_title: suggestion title
    :param suggestion_comment: suggestion comment
    :return: comment body
    """
    return SUGGESTION_COMMENT_STRUCTURE.format(suggestion_title, suggestion_comment)