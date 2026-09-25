from ..agents.reviewer import reviewer_agent
from ..state import ResearchState


def reviewer_node(state: ResearchState) -> dict:
    feedback = reviewer_agent(state["final_report"])
    status = "approved" if "STATUS: APPROVED" in feedback.upper() else "needs_revision"
    return {
        "review_feedback": feedback,
        "review_status": status,
    }
