from .llm import get_llm


def summarizer_agent(topic: str, plan: str, results: str, feedback: str = "") -> str:
    prompt = f"""
Write a clear research report about: {topic}

Research plan:
{plan}

Research findings:
{results}

Previous reviewer feedback:
{feedback or "No previous feedback."}

Synthesize the findings without inventing facts. Include an executive summary,
section headings, key limitations, and a short conclusion.
"""
    return get_llm().invoke(prompt).content
