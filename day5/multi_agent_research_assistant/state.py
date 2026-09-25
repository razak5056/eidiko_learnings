from operator import add
from typing import Annotated, TypedDict


class ResearchResult(TypedDict):
    area: str
    content: str


class ResearchState(TypedDict, total=False):
    topic: str
    research_plan: list[str]
    research_results: Annotated[list[ResearchResult], add]
    final_report: str
    review_feedback: str
    review_status: str
    approval_status: str
    retry_count: int
