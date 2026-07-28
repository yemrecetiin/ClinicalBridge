import os
from langchain_openai import ChatOpenAI
from config import LLM_MODEL_NAME

class BaseAgent:
    def __init__(self, temperature: float = 0.0):
        """
        Initializes the base LLM for the agent.
        Uses ChatOpenAI configured for OpenRouter with the model specified in config.py.
        """
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key or api_key == "your-openrouter-key":
            raise ValueError("OPENROUTER_API_KEY environment variable is missing or invalid.")
            
        self.llm = ChatOpenAI(
            model=LLM_MODEL_NAME,
            temperature=temperature,
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
