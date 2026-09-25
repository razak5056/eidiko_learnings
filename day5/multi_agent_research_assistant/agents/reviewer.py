from .llm import get_llm


def reviewer_agent(report: str) -> str:
    prompt = f"""
Review this research report for accuracy, completeness, clarity, unsupported
claims, and missing limitations:

{report}

Return exactly one status line, either STATUS: APPROVED or
STATUS: NEEDS_REVISION, followed by concise feedback.
"""
    return get_llm().invoke(prompt).content
