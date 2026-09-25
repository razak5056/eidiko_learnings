from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    return ChatGroq(
        model="qwen/qwen3.8-27b",
        temperature=0,
        max_tokens=250,
    )
