from langgraph.graph import StateGraph
from state import State


def process_input(state):
    text = state["user_input"]

    return {
        "processed_text": text.upper()
    }


def generate_response(state):
    return {
        "response": f"Processed text: {state['processed_text']}"
    }


graph = StateGraph(State)


# Add nodes
graph.add_node("process", process_input)
graph.add_node("response", generate_response)


# Add edges
graph.set_entry_point("process")
graph.add_edge("process", "response")
graph.set_finish_point("response")


# Compile graph
app = graph.compile()