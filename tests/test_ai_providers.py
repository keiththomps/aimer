import pytest

from ghost_writer.ai_providers import AIProvider, OpenAIProvider, AnthropicProvider


def test_ai_provider_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AIProvider()


# Tests for OpenAIProvider
def test_openai_provider_send_message():
    provider = OpenAIProvider()
    response = provider.send_message(
        "System prompt", "User prompt", ["file1.txt", "file2.txt"]
    )
    assert response == "OpenAI response"


def test_openai_provider_available_models():
    provider = OpenAIProvider()
    models = provider.available_models()
    assert set(models) == set(["gpt-3.5-turbo", "text-davinci-003", "code-davinci-002"])


# Tests for AnthropicProvider
def test_anthropic_provider_available_models():
    provider = AnthropicProvider(api_key=None, base_url=None, model=None)
    models = provider.available_models()
    assert set(models) == set(["claude-3-sonnet-20240229", "claude-3-opus-20240229"])
