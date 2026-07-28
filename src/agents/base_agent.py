from src.core.llm_client import LLMClient
from src.utils.logger import setup_logger


class BaseAgent:
    """Parent class for all agents to inherit shared configuration."""

    def __init__(self, name: str):
        self.name = name
        self.llm = LLMClient()
        self.logger = setup_logger(self.name)

    def process(self, task: str) -> dict:
        """Abstract method. Every specific agent must implement its own version of this."""
        raise NotImplementedError("Each agent must implement its own process method.")
