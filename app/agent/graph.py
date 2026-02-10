from langgraph.graph import StateGraph
from .state import AgentState
from .tools import calculator, read_file

def planner_node(state: AgentState) -> AgentState:
    state["reasoning_steps"].append("Planner: analyzing user input")
    state["plan"] = "Decide whether a tool is needed"
    return state

def tool_selection_node(state: AgentState) -> AgentState:
    state["reasoning_steps"].append("Tool selector: choosing tool")

    if "calculate" in state["user_input"].lower()
        state["selected_tool"] = "calculator"
        state["tool_input"] = state["user_input"]
    else:
        state["selected_tool"] = None

    return state

def tool_execution_node(state: AgentState) -> AgentState:
    state["reasoning_steps"].append("Tool executor: running tool")

    if state["selected_tool"] == "calculator":
        state["tool_output"] = calculator(state["tool_input"])
    
    return state

def final_response_node(state: AgentState) -> AgentState:
    state["reasoning_steps"].append("Finalizing response")

    if state["tool_output"]:
        state["final_answer"] = f"Result: {state['tool_output']}"
    else:
        state["final_answer"] = "No tool was required."
    
    return state

