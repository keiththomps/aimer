import os
import tempfile
from ghost_writer.prompt_builder import build_prompt

def test_build_prompt_with_multiple_files():
    with tempfile.NamedTemporaryFile(delete=False) as temp1:
        temp1.write(b'This is a file from the prompt.')
        temp1_name = temp1.name

    with tempfile.NamedTemporaryFile(delete=False) as temp2:
        temp2.write(b'This is a file path passed in.')
        temp2_name = temp2.name

    user_prompt = f'User prompt with file path: {temp1_name}'
    files = [temp2_name]

    expected_prompt = f'User prompt with file path: {temp1_name}\n\n--- {temp1_name}\n\nThis is a file from the prompt.\n\n--- {temp2_name}\n\nThis is a file path passed in.'
    actual_prompt = build_prompt(user_prompt, files)

    assert actual_prompt == expected_prompt, f'Expected "{expected_prompt}", but got "{actual_prompt}"'

    os.remove(temp1_name)
    os.remove(temp2_name)

def test_build_prompt_with_relative_file_path():
    with tempfile.NamedTemporaryFile(dir="./temp", delete=False) as temp1:
        temp1.write(b'This is a file from the prompt.')
        relative_name = temp1.name

    print(f'Relative name: {relative_name}')

    user_prompt = f'User prompt with file path: {relative_name}'

    expected_prompt = f'User prompt with file path: {relative_name}\n\n--- {relative_name}\n\nThis is a file from the prompt.'
    actual_prompt = build_prompt(user_prompt)

    assert actual_prompt == expected_prompt, f'Expected "{expected_prompt}", but got "{actual_prompt}"'

    os.remove(relative_name)

