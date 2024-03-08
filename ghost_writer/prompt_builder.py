import re

def build_prompt(user_prompt, files=[]):
    # Extract file paths from the user prompt
    file_paths = re.findall(r'(?:/[\w._-]+)+\b', user_prompt)

    # Read the contents of the files
    file_contents = []
    for file_path in file_paths + files:
        with open(file_path, 'r') as file:
            file_contents.append(f"\n\n--- {file_path}\n\n{file.read()}")

    # Build the prompt
    prompt = user_prompt + ''.join(file_contents)

    return prompt
