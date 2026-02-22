from langgraph.graph import StateGraph
from .state import AgentState
from .tools import calculator, read_file
from .llm_tools import call_ollama, extract_json
import json

def planner_node(state: AgentState) -> AgentState:
    state["reasoning_steps"].append("Planner: analyzing user input")
    state["plan"] = "Decide whether a tool is needed"
    return state

def tool_selection_node(state: AgentState) -> AgentState:
    state["reasoning_steps"].append("Tool selector: using LLM to choose tool")

    prompt = f"""
                You are a tool-using agent. The user input is: "{state['user_input']}".
                Decide:
                1. Which tool should be used (calculator, read_file, or None)
                2. The input to that tool
                Return as JSON: {{ "tool": <tool_name_or_None>, "input": <tool_input_or_null> }}
            """
    try:
        result = call_ollama(prompt)
        #print("[DEBUG] LLM raw result:", repr(result), flush=True)
        tool_data = extract_json(result)
        
        if tool_data:
            state["selected_tool"] = tool_data.get("tool")
            state["tool_input"] = tool_data.get("input")
        
        else:
            state["reasoning_steps"].append("LLM tool selection returned no valid JSON")
            state["selected_tool"] = None
            state["tool_input"] = None
    
    except Exception as e:
        state["reasoning_steps"].append(f"LLM tool selection failed: {e}")
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