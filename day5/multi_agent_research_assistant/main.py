import sys
from pathlib import Path

from langgraph.types import Command

if __package__:
    from .graph import graph
else:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from day5.multi_agent_research_assistant.graph import graph


def main() -> None:
    topic = input("Enter a research topic: ").strip()
    if not topic:
        raise SystemExit("A research topic is required.")

    config = {"configurable": {"thread_id": "research-assistant-1"}}
    request = {"topic": topic, "research_results": [], "retry_count": 0}

    while True:
        interrupted = False
        for event in graph.stream(
            request,
            config=config,
            stream_mode="updates",
        ):
            print("\nEVENT:")
            print(event)
            if "__interrupt__" in event:
                interrupted = True

        if not interrupted:
            break

        decision = input("Approve the report? Type yes or no: ").strip()
        request = Command(resume=decision)

    final_state = graph.get_state(config).values
    print("\nFINAL REPORT\n")
    print(final_state.get("final_report", "No report was produced."))


if __name__ == "__main__":
    main()
