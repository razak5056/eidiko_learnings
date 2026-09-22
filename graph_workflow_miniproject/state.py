from typing import TypedDict


class State(TypedDict):
    user_input: str
    processed_text: str
    response: str