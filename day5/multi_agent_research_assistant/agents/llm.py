from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
    )
