from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langgraph.types import Command
from pydantic import BaseModel, Field

from .graph import graph

app = FastAPI(title="Research Desk API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=4)
jobs: dict[str, dict[str, Any]] = {}
jobs_lock = Lock()


class ResearchRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500)


class ApprovalRequest(BaseModel):
    decision: str


def run_graph(thread_id: str, request: Any) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    interrupted = False
    config = {"configurable": {"thread_id": thread_id}}

    try:
        for event in graph.stream(request, config=config, stream_mode="updates"):
            events.append(event)
            with jobs_lock:
                jobs[thread_id]["events"] = events.copy()
            if "__interrupt__" in event:
                interrupted = True
                with jobs_lock:
                    jobs[thread_id].update(
                        running=False,
                        pending_approval=True,
                        status="approval_required",
                    )
                break
    except Exception as error:
        with jobs_lock:
            jobs[thread_id].update(status="error", error=str(error), running=False)
        return jobs[thread_id]

    values = graph.get_state(config).values
    result = {
        "thread_id": thread_id,
        "events": events,
        "pending_approval": interrupted,
        "report": values.get("final_report", ""),
        "review_feedback": values.get("review_feedback", ""),
        "running": False,
        "status": "approval_required" if interrupted else "complete",
    }
    with jobs_lock:
        jobs[thread_id].update(result)
    return result


def submit_run(thread_id: str, request: Any) -> dict[str, Any]:
    initial = {
        "thread_id": thread_id,
        "events": [],
        "pending_approval": False,
        "report": "",
        "review_feedback": "",
        "running": True,
        "status": "running",
        "error": "",
    }
    with jobs_lock:
        jobs[thread_id] = initial
    executor.submit(run_graph, thread_id, request)
    return initial


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/research/{thread_id}")
def research_status(thread_id: str) -> dict[str, Any]:
    with jobs_lock:
        job = jobs.get(thread_id)
    if job:
        return job

    # Recover completed or interrupted runs after an API process restart.
    try:
        snapshot = graph.get_state({"configurable": {"thread_id": thread_id}})
    except Exception as error:
        raise HTTPException(status_code=404, detail="Research run not found.") from error

    values = snapshot.values
    if not values:
        raise HTTPException(status_code=404, detail="Research run not found.")

    pending_approval = "approval" in snapshot.next
    return {
        "thread_id": thread_id,
        "events": [],
        "pending_approval": pending_approval,
        "report": values.get("final_report", ""),
        "review_feedback": values.get("review_feedback", ""),
        "running": False,
        "status": "approval_required" if pending_approval else "complete",
        "error": "",
    }


@app.post("/research")
def start_research(request: ResearchRequest) -> dict[str, Any]:
    thread_id = f"research-{uuid4().hex}"
    return submit_run(
        thread_id,
        {"topic": request.topic, "research_results": [], "retry_count": 0},
    )


@app.post("/research/{thread_id}/approval")
def approve_research(thread_id: str, request: ApprovalRequest) -> dict[str, Any]:
    if request.decision.lower() not in {"yes", "no"}:
        raise HTTPException(status_code=400, detail="Decision must be yes or no.")
    with jobs_lock:
        missing_job = thread_id not in jobs
    if missing_job:
        recovered = research_status(thread_id)
        with jobs_lock:
            jobs[thread_id] = recovered
    with jobs_lock:
        jobs[thread_id].update(
            running=True,
            pending_approval=False,
            status="running",
        )
    executor.submit(run_graph, thread_id, Command(resume=request.decision.lower()))
    with jobs_lock:
        return jobs[thread_id]
