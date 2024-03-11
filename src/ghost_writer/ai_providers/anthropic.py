from typing import List

from .base import AIProvider

class AnthropicProvider(AIProvider):
    def send_message(self, system_prompt: str, user_prompt: str, files: List[str] = []) -> str:
        # Implementation to send the prompt to Anthropic API and receive a response
        return "Anthropic response"

    def available_models(self) -> List[str]:
        # Implementation to get a list of available Anthropic models
        return ["claude-v1.0", "claude-v1.3"]
