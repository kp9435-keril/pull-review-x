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

def generate_html_table(table_data: dict[str, Any]) -> str:
    """
    generate html table from table data
    :param table_data: table data
    :return: html table
    """
    table = f"""<table>"""
    for category, suggestions in table_data.items():
        table += f"""
        <tr>
            <td>{category.replace("_", " ").title()}</td>
        """
        if(suggestions):
            table += f"""
            <td>
                <ul>
            """
            for suggestion in suggestions:
                table += f"""
                <li>{suggestion}</li>
                """
            table += f"""
                </ul>
            </td>
            """
        else:
            table += f"""
            <td>No suggestions</td>
            """
        
    
    table += f"""</table>"""
    print(table)