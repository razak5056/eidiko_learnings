import ast
import operator

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool

from .llm import get_llm


@tool
def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression for research calculations."""
    allowed_operators = {
        ast.Add: operator.add,
        ast.Div: operator.truediv,
        ast.Mult: operator.mul,
        ast.Sub: operator.sub,
        ast.USub: operator.neg,
    }

    def evaluate(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](evaluate(node.operand))
        raise ValueError("Only basic arithmetic is supported.")

    try:
        return str(evaluate(ast.parse(expression, mode="eval")))
    except (SyntaxError, ValueError, ZeroDivisionError) as error:
        return f"Calculation error: {error}"


@tool
def research_source_guide(query: str, topn: int = 5, source: str = "") -> str:
    """Return trustworthy source guidance for a research query."""
    del topn
    area = query.lower()
    guides = {
        "technical foundations": (
            "Prefer official statistical agencies, peer-reviewed methodology papers, "
            "UN data portals, and World Bank indicators."
        ),
        "benefits and business impact": (
            "Prefer company filings, government economic surveys, World Bank data, "
            "and reputable industry reports."
        ),
        "real-world applications and future trends": (
            "Prefer government program reports, UN projections, peer-reviewed studies, "
            "and clearly labelled scenario forecasts."
        ),
    }
    guides = guides.get(
        area,
        "Prefer primary government data, international organizations, and peer-reviewed research.",
    )
    if source:
        return f"{guides} Suggested source: {source}. Query: {query}."
    return guides


TOOLS = [calculate, research_source_guide]


def researcher_agent(topic: str, area: str) -> str:
    prompt = f"""
Research the topic below from the perspective of {area}.

Topic: {topic}

Use accurate, accessible language. Explain important evidence, limitations,
and concrete examples. Do not invent citations. Use the source guide tool and
the calculator when a calculation would make the explanation clearer.
"""
    tool_llm = get_llm().bind_tools(TOOLS)
    messages = [
        SystemMessage(
            content="You are a careful research analyst. Use tools when useful, then answer plainly."
        ),
        HumanMessage(content=prompt),
    ]

    for _ in range(3):
        response = tool_llm.invoke(messages)
        messages.append(response)
        if not response.tool_calls:
            return response.content

        for tool_call in response.tool_calls:
            selected_tool = next(tool for tool in TOOLS if tool.name == tool_call["name"])
            result = selected_tool.invoke(tool_call["args"])
            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )

    tool_results = "\n".join(
        message.content
        for message in messages
        if isinstance(message, ToolMessage)
    )
    final_prompt = f"""
Answer this research request:
{prompt}

Tool results:
{tool_results}

Use the tool results where relevant. Do not invent citations.
"""
    return get_llm().invoke(final_prompt).content
