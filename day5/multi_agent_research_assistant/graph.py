import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, StateGraph

from .nodes.approval_node import approval_node
from .nodes.correction_node import correction_node
from .nodes.manager_node import manager_node
from .nodes.researcher_nodes import business_node, technical_node, trends_node
from .nodes.reviewer_node import reviewer_node
from .nodes.summarizer_node import summarizer_node
from .routing.router import approval_router, review_router
from .state import ResearchState

load_dotenv(Path(__file__).resolve().parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is required. Example: "
        "postgresql://postgres:password@localhost:5432/research_assistant"
    )

builder = StateGraph(ResearchState)
builder.add_node("manager", manager_node)
builder.add_node("technical_research", technical_node)
builder.add_node("business_research", business_node)
builder.add_node("trends_research", trends_node)
builder.add_node("summarizer", summarizer_node)
builder.add_node("reviewer", reviewer_node)
builder.add_node("correction", correction_node)
builder.add_node("approval", approval_node)

builder.add_edge(START, "manager")
builder.add_edge("manager", "technical_research")
builder.add_edge("manager", "business_research")
builder.add_edge("manager", "trends_research")
builder.add_edge("technical_research", "summarizer")
builder.add_edge("business_research", "summarizer")
builder.add_edge("trends_research", "summarizer")
builder.add_edge("summarizer", "reviewer")
builder.add_conditional_edges(
    "reviewer",
    review_router,
    {"correction": "correction", "approval": "approval"},
)
builder.add_edge("correction", "summarizer")
builder.add_conditional_edges(
    "approval",
    approval_router,
    {"finish": END, "correction": "correction"},
)

connection = psycopg.connect(DATABASE_URL, autocommit=True)
checkpointer = PostgresSaver(connection)
checkpointer.setup()

graph = builder.compile(checkpointer=checkpointer)
