from langgraph.graph import StateGraph
from typing import TypedDict
class state(TypedDict):
    name: str
    role: str
    experience_years: int
    decision: str


def receive_application(state):
    state['name'] = input("Enter your name: ")
    state['role'] = input("Enter the role you are applying for: ")
def screen_resume(state):
    experience_years=int(input("Enter your years of experience: "))
    state['experience_years'] = experience_years
    if experience_years >= 2:
        state['decision'] = "Selected"
    else:
        state['decision'] = "Rejected"
def send_decision(state):
    print(f"Application Decision for {state['name']}: {state['decision']}") 


graph = StateGraph(state)

graph.add_node("Receive Application", receive_application)
graph.add_node("Screen Resume", screen_resume)
graph.add_node("Send Decision", send_decision)


graph.set_entry_point("Receive Application")
graph.add_edge("Receive Application", "Screen Resume")
graph.add_edge("Screen Resume", "Send Decision")
graph.set_finish_point("Send Decision")


app=graph.compile()
result=app.invoke(name="prem chand",role="ai/ml",experience_years=3,decision="")
print(result)