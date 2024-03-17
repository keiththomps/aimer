import json
import os
from typing import List, Optional
from xml.etree import ElementTree as ET

from anthropic import Anthropic

from aimer.prompts import build_prompt
from .base import AIProvider


class AnthropicProvider(AIProvider):
    def __init__(
        self, api_key: Optional[str], base_url: Optional[str], model: Optional[str]
    ):
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        base_url = base_url or os.getenv("ANTHROPIC_BASE_URL")
        if base_url:
            self.client = Anthropic(api_key=api_key, base_url=base_url)
        else:
            self.client = Anthropic(api_key=api_key)
        self.model = model or self.available_models()[0]
        self.messages = []
        self.tool_definitions = self.read_tool_definitions()

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
            max_tokens=4096,  # Max allowed by Claude 3
            system=f"{system_prompt}\n{self.tool_definitions}",
            messages=self.messages,
            model=self.model,
        )

        content = message.content[0].text

        self.messages.append({"role": "assistant", "content": content})

        function_calls = self.extract_function_calls(content)
        functions = self.parse_function_calls(function_calls)

        return functions

    def available_models(self) -> List[str]:
        return [
            "claude-3-haiku-20240307",
            "claude-3-sonnet-20240229",
            "claude-3-opus-20240229",
        ]

    def read_tool_definitions(self) -> str:
        def_path = os.path.join(
            os.path.dirname(__file__), "anthropic_tool_definitions.txt"
        )
        with open(def_path, encoding="utf-8") as f:
            return f.read().strip()

    def extract_function_calls(self, content: str) -> str:
        call_start = content.find("<function_calls>")
        call_end = content.find("</function_calls>") + len("</function_calls>")
        return content[call_start:call_end]

    def parse_function_calls(self, function_calls: str) -> List[dict]:
        try:
            function_calls = ET.fromstring(function_calls)
        except ET.ParseError:
            print(f"Could not parse function calls {function_calls}")
            return []
        data = []
        for invocation in function_calls.findall("invoke"):
            invoke_data = {"kwargs": {}}
            for child in invocation:
                if child.tag == "tool_name":
                    invoke_data["name"] = child.text
                elif child.tag == "parameters":
                    for param in child:
                        invoke_data["kwargs"][param.tag] = param.text
            data.append(invoke_data)
        return data
