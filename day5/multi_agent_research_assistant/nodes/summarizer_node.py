from ..agents.summarizer import summarizer_agent
from ..state import ResearchState

MAX_FINDING_CHARS = 3500
MAX_FEEDBACK_CHARS = 2500


def _trim(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return f"{text[:limit]}\n[Content truncated to fit the model context limit.]"


def summarizer_node(state: ResearchState) -> dict:
    findings = "\n\n".join(
        f"{item['area'].title()}:\n{_trim(item['content'], MAX_FINDING_CHARS)}"
        for item in state.get("research_results", [])
    )
    report = summarizer_agent(
        state["topic"],
        "\n".join(state.get("research_plan", [])),
        findings,
        _trim(state.get("review_feedback", ""), MAX_FEEDBACK_CHARS),
    )
    return {"final_report": report}
