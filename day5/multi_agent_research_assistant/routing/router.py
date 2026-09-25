from ..nodes.correction_node import MAX_RETRIES
from ..state import ResearchState


def review_router(state: ResearchState) -> str:
    if state.get("review_status") == "approved":
        return "approval"
    if state.get("retry_count", 0) < MAX_RETRIES:
        return "correction"
    return "approval"


def approval_router(state: ResearchState) -> str:
    decision = state.get("approval_status", "").lower()
    return "finish" if decision in {"yes", "y", "approve", "approved"} else "correction"
