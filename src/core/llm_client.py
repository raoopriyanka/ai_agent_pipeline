from openai import OpenAI
from src.core.config import Config

class LLMClient:
    """
    A unified interface for interacting with LLMs.
    Supports any OpenAI-compatible API (OpenAI, Groq, vLLM, etc.)
    """
    
    def __init__(self):
        # The OpenAI python package natively supports custom base URLs
        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.LLM_BASE_URL
        )
        self.model = Config.MODEL_NAME

    def chat(self, messages: list, temperature: float = 0.7) -> str:
        """
        Sends a standard message payload to the LLM.
        
        Args:
            messages (list): A list of dictionaries containing role/content.
            temperature (float): Creativity threshold (0.0 to 2.0).
            
        Returns:
            str: The text content of the LLM's response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            # We will implement proper logging later, but for now we print the crash
            print(f"CRITICAL API ERROR: {e}")
            raise