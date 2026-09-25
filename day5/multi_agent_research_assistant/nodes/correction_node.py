from ..state import ResearchState

MAX_RETRIES = 3


def correction_node(state: ResearchState) -> dict:
    return {"retry_count": state.get("retry_count", 0) + 1}
