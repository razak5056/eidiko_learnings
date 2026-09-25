from ..agents.researcher import researcher_agent
from ..state import ResearchState


def _research(state: ResearchState, area: str) -> dict:
    result = researcher_agent(state["topic"], area)
    return {"research_results": [{"area": area, "content": result}]}


def technical_node(state: ResearchState) -> dict:
    return _research(state, "technical foundations")


def business_node(state: ResearchState) -> dict:
    return _research(state, "benefits and business impact")


def trends_node(state: ResearchState) -> dict:
    return _research(state, "real-world applications and future trends")
