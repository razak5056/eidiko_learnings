from .llm import get_llm


def manager_agent(topic: str) -> str:
    prompt = f"""
Create a concise research plan for this topic: {topic}

The plan must cover exactly these areas:
1. Technical foundations
2. Benefits and business impact
3. Real-world applications and future trends

Return the plan as plain text.
"""
    return get_llm().invoke(prompt).content
