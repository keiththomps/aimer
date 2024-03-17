from abc import ABC, abstractmethod
from typing import List


class AIProvider(ABC):
    """
    Abstract base class for AI providers.
    """

    @abstractmethod
    def send_message(
        self, system_prompt: str, user_prompt: str, files: List[str] = []
    ) -> str:
        """
        Send a message to the AI provider and receive a response.

        Args:
            system_prompt (str): The system prompt to use.
            user_prompt (str): The user's prompt or message.
            files (List[str], optional): A list of file paths to provide additional context.

        Returns:
            str: The response from the AI provider.
        """
        pass

    @abstractmethod
    def available_models(self) -> List[str]:
        """
        Get a list of available models for the AI provider.

        Returns:
            List[str]: A list of available model names.
        """
        pass
