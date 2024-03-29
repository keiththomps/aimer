import pytest

from aimer.ai_providers import AIProvider, OpenAIProvider, AnthropicProvider


def test_ai_provider_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AIProvider()


# Tests for OpenAIProvider
def test_openai_provider_available_models():
    provider = OpenAIProvider(api_key="some-key", base_url=None, model=None)
    models = provider.available_models()
    assert set(models) == set(["gpt-3.5-turbo", "gpt-4-turbo-preview"])


# Tests for AnthropicProvider
def test_anthropic_provider_available_models():
    provider = AnthropicProvider(api_key="some-key", base_url=None, model=None)
    models = provider.available_models()
    assert set(models) == set(
        [
            "claude-3-haiku-20240307",
            "claude-3-sonnet-20240229",
            "claude-3-opus-20240229",
        ]
    )
