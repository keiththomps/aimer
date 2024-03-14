import os
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory, NamedTemporaryFile

from ghost_writer.prompts import (
    build_prompt,
    fetch_system_prompt,
    build_system_prompt,
    extract_paths,
)


def test_build_system_prompt():
    project_languages = "Python, JavaScript"
    project_frameworks = "Django, React"
    comments_in_code = True
    automated_tests = True
    testing_frameworks = ["pytest", "jest"]
    example_test_case = "# Example test case for the sum function\ndef test_sum():\n    assert sum([1, 2, 3]) == 6, 'Should be 6'"

    expected_prompt = """You are an expert at programming in Python, JavaScript, and the following frameworks: Django, React. You always produce code that follows best practices and idioms from the target programming language. You are expected to write code that is clear, concise, and maintainable.. Please include comments in the code to explain what the code does. Please include automated tests for the code using the following testing frameworks: pytest, jest.

Here is an example of how I would like the tests to be written:
# Example test case for the sum function
def test_sum():
    assert sum([1, 2, 3]) == 6, 'Should be 6'"""

    assert (
        build_system_prompt(
            project_languages,
            project_frameworks,
            comments_in_code,
            automated_tests,
            testing_frameworks,
            example_test_case,
        )
        == expected_prompt
    )


def test_build_prompt_with_multiple_files():
    with NamedTemporaryFile(delete=False) as temp1:
        temp1.write(b"This is a file from the prompt.")
        temp1_name = temp1.name

    with NamedTemporaryFile(delete=False) as temp2:
        temp2.write(b"This is a file path passed in.")
        temp2_name = temp2.name

    user_prompt = f"User prompt with file path: {temp1_name}"
    files = [temp2_name]

    expected_prompt = f"User prompt with file path: {temp1_name}\n\n--- {temp1_name}\n\nThis is a file from the prompt.\n\n--- {temp2_name}\n\nThis is a file path passed in."
    actual_prompt = build_prompt(user_prompt, files)

    assert (
        actual_prompt == expected_prompt
    ), f'Expected "{expected_prompt}", but got "{actual_prompt}"'

    os.remove(temp1_name)
    os.remove(temp2_name)


def test_build_prompt_with_relative_file_path():
    with TemporaryDirectory() as tmpdir:
        with NamedTemporaryFile(dir=tmpdir, delete=False) as temp1:
            temp1.write(b"This is a file from the prompt.")
            relative_name = temp1.name

        print(f"Relative name: {relative_name}")

        os.chdir(tmpdir)

        user_prompt = f"User prompt with file path: {relative_name}"
        expected_prompt = f"User prompt with file path: {relative_name}\n\n--- {relative_name}\n\nThis is a file from the prompt."
        actual_prompt = build_prompt(user_prompt)

        assert (
            actual_prompt == expected_prompt
        ), f'Expected "{expected_prompt}", but got "{actual_prompt}"'

        os.remove(relative_name)


def test_fetch_system_prompt_valid_path():
    with TemporaryDirectory() as tmpdir:
        prompt_path = os.path.join(tmpdir, "test_prompt.md")
        with open(prompt_path, "w") as file:
            file.write("This is a test prompt.")

        prompt_text = fetch_system_prompt(prompt_path)
        assert prompt_text == "This is a test prompt."


def test_fetch_system_prompt_local_directory():
    with TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, ".ghost"), exist_ok=True)
        prompt_file = os.path.join(tmpdir, ".ghost", "test_prompt.txt")
        with open(prompt_file, "w") as file:
            file.write("This is a test prompt.")

        os.chdir(tmpdir)
        prompt_text = fetch_system_prompt("test_prompt")
        assert prompt_text == "This is a test prompt."


def test_fetch_system_prompt_home_directory(monkeypatch):
    with TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)  # Change the current working directory
        monkeypatch.setattr("pathlib.Path.home", lambda: Path(tmpdir))
        os.makedirs(os.path.join(tmpdir, ".ghost"), exist_ok=True)
        prompt_file = os.path.join(tmpdir, ".ghost", "default_prompt.txt")
        with open(prompt_file, "w") as file:
            file.write("This is a test prompt.")

        prompt_text = fetch_system_prompt("default_prompt")
        assert prompt_text == "This is a test prompt."


def test_fetch_system_prompt_file_not_found(monkeypatch):
    with TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)  # Change the current working directory
        monkeypatch.setattr("pathlib.Path.home", lambda: Path(tmpdir))

        with pytest.raises(FileNotFoundError) as exc_info:
            fetch_system_prompt("non_existent_prompt")

        # The last path is from monkey patching $HOME
        expected_error_message = f"""System prompt file 'non_existent_prompt.txt' not found in the following paths:
            \tnon_existent_prompt.txt
            \t#{tmpdir}/.ghost/non_existent_prompt.txt
            \t#{tmpdir}/.ghost/non_existent_prompt.txt"""


def test_extract_paths_multiple_paths():
    text = "Here are some paths: /path/to/file.py, ./src/cli.py, and src/utils.py"
    matches = extract_paths(text)
    assert matches == ["/path/to/file.py", "./src/cli.py", "src/utils.py"]


def test_extract_paths_single_path():
    text = "refactor /path/to/file.py"
    matches = extract_paths(text)
    assert matches == ["/path/to/file.py"]


def test_extract_paths_no_path():
    text = "There are no paths here."
    matches = extract_paths(text)
    assert matches == []
