"""
Module responsible for building, and fetching various LLM prompts.
"""

import re
import os
from pathlib import Path
from typing import List, Optional


# pylint: disable=too-many-arguments
def build_system_prompt(
    project_languages: str,
    project_frameworks: str,
    comments_in_code: bool,
    automated_tests: bool,
    testing_frameworks: List[str],
    example_test_case: Optional[str],
) -> str:
    """
    Construct a tailored system prompt to send with LLM requests to better set the
    stage for the user's current project.
    """
    system_prompt = f"""You are an expert at programming in {project_languages},"""

    if project_frameworks:
        system_prompt += f" and the following frameworks: {project_frameworks}."

    system_prompt += (
        " You always produce code that follows best practices "
        "and idioms from the target programming language. "
        "You are expected to write code that is clear, concise, and maintainable."
    )

    if comments_in_code:
        system_prompt += (
            ". Please include comments in the code to explain what the code does."
        )
    else:
        system_prompt += ". Do not include inline comments in the code that you write."

    if automated_tests:
        system_prompt += (
            " Please include automated tests for the code "
            f"using the following testing frameworks: {', '.join(testing_frameworks)}."
        )
        if example_test_case:
            system_prompt += (
                "\n\nHere is an example of how I would like "
                f"the tests to be written:\n{example_test_case}"
            )
    else:
        system_prompt += " Automated tests are not required."

    return system_prompt


def fetch_system_prompt(prompt_name: str) -> str:
    """
    Fetches the system prompt from the specified file.

    Args:
        prompt_name (str): The name or path of the system prompt file.

    Returns:
        str: The system prompt text.

    Raises:
        FileNotFoundError: If the file is not found in the specified path,
        './.aimer/', or '~/.aimer/'.
    """
    # Check if the prompt_name has an extension
    prompt_name = prompt_name or "default_prompt.txt"
    if Path(prompt_name).suffix:
        prompt_file_name = prompt_name
    else:
        prompt_file_name = f"{prompt_name}.txt"

    # If prompt_name is a path, check if the file exists
    if Path(prompt_file_name).is_file():
        try:
            with open(prompt_file_name, "r", encoding="utf-8") as file:
                prompt_text = file.read().strip()
            return prompt_text
        except FileNotFoundError:
            pass

    # Check in the local '.aimer' directory
    local_prompt_file = Path(os.getcwd(), ".aimer", prompt_file_name)
    if local_prompt_file.is_file():
        try:
            with open(local_prompt_file, "r", encoding="utf-8") as file:
                prompt_text = file.read().strip()
            return prompt_text
        except FileNotFoundError:
            pass

    # Check in the user's '~/.aimer' directory
    home_prompt_file = Path(Path.home(), ".aimer", prompt_file_name)
    if home_prompt_file.is_file():
        try:
            with open(home_prompt_file, "r", encoding="utf-8") as file:
                prompt_text = file.read().strip()
            return prompt_text
        except FileNotFoundError:
            pass

    searched_paths = "\n".join(
        [
            f"\t{str(prompt_file_name)}",
            f"\t{str(local_prompt_file)}",
            f"\t{str(home_prompt_file)}",
        ]
    )
    raise FileNotFoundError(
        f"System prompt file '{prompt_file_name}' not found "
        f"in the following paths:\n{searched_paths}"
    )


def build_prompt(
    user_prompt: str,
    files: Optional[list] = None,
) -> str:
    """
    Builds a prompt by combining the system prompt, user prompt, and contents of specified files.

    Args:
        user_prompt (str): The user prompt text.
        files (list, optional): A list of file paths to include in the prompt. Defaults to [].

    Returns:
        str: The combined prompt text.

    The function first extracts file paths from the `user_prompt` using a
    regular expression pattern. It then reads the contents of the files specified
    in `files` and the extracted file paths. The file contents are appended to the
    prompt with a separator (--- file_path) for each file. Finally, the function
    combines the `user_prompt` and file contents into a single string.
    """
    files = files or []
    file_paths = extract_paths(user_prompt)

    file_contents = []
    for file_path in file_paths + files:
        with open(file_path, "r", encoding="utf-8") as file:
            file_contents.append(f"\n\n--- {file_path}\n\n{file.read()}")

    prompt = user_prompt + "".join(file_contents)

    return prompt


def extract_paths(text):
    words = text.split()
    paths = []

    for word in words:
        # Remove trailing punctuation that might be attached to paths
        trimmed_word = word.rstrip(",.?!")

        # Simple heuristic to identify potential paths
        if "/" in trimmed_word or trimmed_word.startswith("."):
            paths.append(trimmed_word)

    return paths
