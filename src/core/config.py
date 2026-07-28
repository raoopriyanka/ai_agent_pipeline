import os
from dotenv import load_dotenv

# Load variables from the .env file into the system's environment variables
load_dotenv()

class Config:
    """Centralized configuration for the AI Pipeline."""
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Using a base URL allows us to easily swap out OpenAI for local models 
    # (like vLLM or Ollama) or other compatible APIs.
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")
    
    @classmethod
    def validate(cls):
        """Fails fast if critical configurations are missing."""
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == "your_openai_api_key_here":
            raise ValueError("CRITICAL: OPENAI_API_KEY is not set correctly in the .env file.")

# Validate configuration on import so the app crashes immediately if misconfigured
Config.validate()