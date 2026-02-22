import os
from agent.graph import build_graph
from agent.state import AgentState

# Load environment variables (from .env file)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

if not OLLAMA_BASE_URL or not OLLAMA_MODEL:
    raise ValueError("OLLAMA_BASE_URL and OLLAMA_MODEL must be set in .env")

def main():
    # Build the workflow (graph)
    workflow = build_graph()

    while True:
        user_input = input("Enter your request (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting agent.")
            break

        # Minimal initial state for this input
        state: AgentState = {
            "user_input": user_input,
            "plan": None,
            "selected_tool": None,
            "tool_input": None,
            "tool_output": None,
            "reasoning_steps": [],
            "step_count": 0,
            "max_steps": 5,
            "final_answer": None,
        }

        # Run the workflow
        final_state = workflow.invoke(state)

        # Print output
        print("[Workflow] Final Answer:", final_state["final_answer"])
        print("[Workflow] Tool Output:", final_state["tool_output"])
        print("[Workflow] Reasoning Steps:")
        for step in final_state["reasoning_steps"]:
            print("-", step)
        print("\n---\n")

if __name__ == "__main__":
    main()
