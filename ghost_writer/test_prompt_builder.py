import os
from .prompt_builder import build_prompt

def test_build_prompt():
    # Create a temporary file for testing
    with open('temp.txt', 'w') as file:
        file.write('This is a test file.')

    base_prompt = 'Base prompt.'
    user_prompt = 'User prompt with file path: temp.txt'
    files = ['temp.txt']

    expected_prompt = 'Base prompt. User prompt with file path: temp.txt This is a test file.'
    actual_prompt = build_prompt(base_prompt, user_prompt, files)

    assert actual_prompt == expected_prompt, f'Expected "{expected_prompt}", but got "{actual_prompt}"'

    # Delete the temporary file
    os.remove('temp.txt')
