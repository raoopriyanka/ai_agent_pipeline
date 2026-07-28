import tiktoken
from src.core.config import Config

def count_tokens(text: str, model_name: str = Config.MODEL_NAME) -> int:
    """
    Calculates the exact number of tokens a string will consume.
    
    Args:
        text (str): The input text to tokenize.
        model_name (str): The model encoding to use.
        
    Returns:
        int: The number of tokens.
    """
    try:
        # Get the specific encoding for the chosen model (e.g., cl100k_base for GPT-4/3.5)
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        # Fallback encoding if the model is not explicitly recognized by tiktoken
        print(f"Warning: Model {model_name} not found. Using default encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
        
    return len(encoding.encode(text))

# Simple execution block for manual testing
if __name__ == "__main__":
    sample_text = "As a Senior AI Engineer, I optimize pipelines for efficiency."
    tokens = count_tokens(sample_text)
    print(f"Sample Text: '{sample_text}'")
    print(f"Token Count: {tokens}")