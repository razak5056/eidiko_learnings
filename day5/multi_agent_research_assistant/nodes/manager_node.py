from ..agents.manager import manager_agent
from ..state import ResearchState


def manager_node(state: ResearchState) -> dict:
    plan = manager_agent(state["topic"])
    return {"research_plan": [plan]}
