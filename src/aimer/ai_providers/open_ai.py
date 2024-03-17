import json
import os

from json import JSONDecoder
from typing import List, Optional

from openai import OpenAI

from aimer.prompts import build_prompt
from .base import AIProvider


class OpenAIProvider(AIProvider):
    def __init__(
        self, api_key: Optional[str], base_url: Optional[str], model: Optional[str]
    ):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.model = model or self.available_models()[0]
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)
        self.messages = []
        self.tool_definitions = self.read_tool_definitions()

    def available_models(self) -> List[str]:
        return ["gpt-3.5-turbo", "gpt-4-turbo-preview"]

    def send_message(
        self, system_prompt: str, user_prompt: str, files: List[str] = []
    ) -> List[dict]:
        # Implementation to send the prompt to Anthropic API and receive a response
        self.messages.append(
            {
                "role": "user",
                "content": f"{system_prompt}\n{build_prompt(user_prompt, files)}",
            }
        )

        if os.getenv("DEBUG"):
            print(f"Sending message {json.dumps(self.messages, indent=2)}")

        response = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            tools=self.tool_definitions,
            tool_choice="auto",
        )

        response_message = response.choices[0].message

        self.messages.append(response_message)

        function_calls = self.extract_function_calls(response_message.tool_calls)

        return function_calls

    def extract_function_calls(self, tool_calls: []) -> List[dict]:
        results = []

        if not tool_calls:
            return results

        for tool_call in tool_calls:
            func = {}

            func["name"] = tool_call.function.name
            func["kwargs"] = json.loads(tool_call.function.arguments)

            results.append(func)
        return results

    def read_tool_definitions(self) -> str:
        def_path = os.path.join(
            os.path.dirname(__file__), "open_ai_tool_definitions.json"
        )
        with open(def_path, encoding="utf-8") as f:
            return JSONDecoder().decode(f.read())
