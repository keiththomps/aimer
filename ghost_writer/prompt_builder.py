import re

def build_prompt(base_prompt, user_prompt, files):
    # Extract file paths from the user prompt
    file_paths = re.findall(r'\b(?:[a-z]:\)?(?:[\w.]+\)*\w+\.\w+\b', user_prompt)

    # Read the contents of the files
    file_contents = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            file_contents.append(file.read())

    # Build the GPT prompt
    gpt_prompt = base_prompt + ' ' + user_prompt + ' ' + ' '.join(file_contents)

    return gpt_prompt
