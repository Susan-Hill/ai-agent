from langgraph.graph import StateGraph
from .state import AgentState
from .tools import calculator, read_file

def planner_node(state: AgentState) -> AgentState:
    state["reasoning_steps"].append("Planner: analyzing user input")
    state["plan"] = "Decide whether a tool is needed"
    return state

def tool_selection_node(state: AgentState) -> AgentState:
    state["reasoning_steps"].append("Tool selector: choosing tool")

    user_input = state["user_input"].lower()

    if "calculate" in user_input:
        state["selected_tool"] = "calculator"
        expression = user_input.split("calculate", 1)[1].strip()
        state["tool_input"] = expression

    else:
        state["selected_tool"] = None
        state["tool_input"] = None
        
    return state

def tool_execution_node(state: AgentState) -> AgentState:
    state["reasoning_steps"].append("Tool executor: running tool")

    if state["selected_tool"] == "calculator":
        result = calculator(state["tool_input"])
        state["tool_output"] = result
    
    elif state["selected_tool"] == "read_file":
        result = read_file(state["tool_input"])
        state["tool_output"] = result
    
    else:
        state["tool_output"] = None
    
    return state

def final_response_node(state: AgentState) -> AgentState:
    state["reasoning_steps"].append("Finalizing response")

    if state["tool_output"]:
        state["final_answer"] = f"Result: {state['tool_output']}"
    else:
        state["final_answer"] = "No tool was required."
    
    return state

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("tool_selector", tool_selection_node)
    workflow.add_node("tool_executor", tool_execution_node)
    workflow.add_node("final", final_response_node)

    workflow.set_entry_point("planner")

    workflow.add_edge("planner", "tool_selector")
    workflow.add_edge("tool_selector", "tool_executor")
    workflow.add_edge("tool_executor", "final")

    return workflow.compile()