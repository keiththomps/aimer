from json import JSONDecoder
from typing import List, Optional

from openai import OpenAI

from .base import AIProvider


class OpenAIProvider(AIProvider):
    def __init__(
        self, api_key: Optional[str], base_url: Optional[str], model: Optional[str]
    ):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        base_url = base_url or os.getenv("OPENAI_BASE_URL")
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)
        self.model = model or self.available_models()[0]
        self.messages = []
        self.tool_definitions = self.read_tool_definitions()

    def available_models(self) -> List[str]:
        return ["gpt-3.5-turbo", "text-davinci-003", "code-davinci-002"]

    def send_message(
        self, system_prompt: str, user_prompt: str, files: List[str] = []
    ) -> List[dict]:
        # Implementation to send the prompt to Anthropic API and receive a response
        self.messages.append(
            {
                "role": "user",
                "content": build_prompt(user_prompt, files),
            }
        )

        if os.getenv("DEBUG"):
            print(f"Sending message {json.dumps(self.messages, indent=2)}")

        message = self.client.messages.create(
            system=f"{system_prompt}\n{self.tool_definitions}",
            messages=self.messages,
            model=self.model,
            tools=self.tool_definitions,
            tool_choice="auto"
        )

        content = message.content[0].text

        self.messages.append({"role": "assistant", "content": content})

        function_calls = self.extract_function_calls(content)
        functions = self.parse_function_calls(function_calls)

        return functions

    def read_tool_definitions(self) -> str:
        def_path = os.path.join(
            os.path.dirname(__file__), "openai_tool_definitions.json"
        )
        with open(def_path, encoding="utf-8") as f:
            return JSONDecoder().decode(f.read())
