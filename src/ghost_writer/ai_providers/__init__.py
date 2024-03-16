from .base import AIProvider
from .open_ai import OpenAIProvider
from .anthropic import AnthropicProvider


def get_provider(provider: str, model: str) -> AIProvider:
    if provider.lower() == "openai":
        return OpenAIProvider(None, None, model)
    elif provider.lower() == "anthropic":
        return AnthropicProvider(None, None, model)
    else:
        raise ValueError(f"Unknown provider: {provider}")
