
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# Load environment variables from the .env file.
load_dotenv()


def get_llm() -> ChatOpenAI:
    """
    Create and configure the OpenAI model used by our agents.

    The model name comes from the OPENAI_MODEL environment variable.
    If it is not configured, GPT-4.1-mini is used by default.
    """
    model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    return ChatOpenAI(
        model=model_name,
        temperature=0,
    )
