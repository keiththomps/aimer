import json
import os
from typing import List, Optional

from anthropic import Anthropic

from ghost_writer.prompts import build_prompt
from .base import AIProvider


class AnthropicProvider(AIProvider):
    def __init__(
        self, api_key: Optional[str], base_url: Optional[str], model: Optional[str]
    ):
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        base_url = base_url or os.getenv("ANTHROPIC_BASE_URL")
        self.client = Anthropic(api_key=api_key, base_url=base_url)
        self.model = model or "claude-3-opus-20240229"
        self.messages = []
        self.function_definitions = self.read_function_definitions()

    def send_message(
        self, system_prompt: str, user_prompt: str, files: List[str] = []
    ) -> str:
        # Implementation to send the prompt to Anthropic API and receive a response
        self.messages.append(
            {
                "role": "user",
                "content": build_prompt(
                    system_prompt, user_prompt, self.function_definitions, files
                ),
            }
        )
        message = self.client.messages.create(messages=self.messages, model=self.model)

        return message.content

    def available_models(self) -> List[str]:
        return ["claude-3-opus-20240229"]

    def read_function_definitions(self) -> str:
        def_path = os.path.join(
            os.path.dirname(__file__), "anthropic_function_definitions.txt"
        )
        with open(def_path, encoding="utf-8") as f:
            return f.read().strip()
