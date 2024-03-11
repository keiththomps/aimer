from typing import List

from .base import AIProvider

class OpenAIProvider(AIProvider):
    def send_message(self, system_prompt: str, user_prompt: str, files: List[str] = []) -> str:
        # Implementation to send the prompt to OpenAI API and receive a response
        return "OpenAI response"

    def available_models(self) -> List[str]:
        # Implementation to get a list of available OpenAI models
        return ["gpt-3.5-turbo", "text-davinci-003", "code-davinci-002"]
