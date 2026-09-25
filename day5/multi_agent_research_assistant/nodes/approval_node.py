from langgraph.types import interrupt

from ..state import ResearchState


def approval_node(state: ResearchState) -> dict:
    decision = interrupt(
        {
            "message": "Approve this research report? Reply yes or no.",
            "report": state["final_report"],
        }
    )
    return {"approval_status": str(decision).strip().lower()}
