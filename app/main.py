import os
import json
import logging
from datetime import datetime
from agent.graph import build_graph
from agent.state import AgentState
from dotenv import load_dotenv

# Load environment variables (from .env file)
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

if not OLLAMA_BASE_URL or not OLLAMA_MODEL:
    raise ValueError("OLLAMA_BASE_URL and OLLAMA_MODEL must be set in .env")

# Log file path
log_dir = "/logs"  # this will mount as a Docker volume for persistence
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),           # Console output
        logging.FileHandler(log_file)      # File output
    ]
)

logger = logging.getLogger(__name__)

# Save reasoning history function
LOG_HISTORY_DIR = "/logs/history"
os.makedirs(LOG_HISTORY_DIR, exist_ok=True)

def save_reasoning_history(state: dict):
    """
    Save reasoning history of a workflow run to a JSON file.
    Filename includes timestamp and sanitized user input.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Keep only alphanumeric, _, - characters to avoid filename issues
    user_input_safe = "".join(c for c in state["user_input"] if c.isalnum() or c in "_-")[:20]
    filename = os.path.join(LOG_HISTORY_DIR, f"{timestamp}_{user_input_safe}.json")

    data_to_save = {
        "user_input": state["user_input"],
        "selected_tool": state.get("selected_tool"),
        "tool_input": state.get("tool_input"),
        "tool_output": state.get("tool_output"),
        "final_answer": state.get("final_answer"),
        "reasoning_steps": state.get("reasoning_steps"),
    }

    with open(filename, "w") as f:
        json.dump(data_to_save, f, indent=4)

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

        # Save reasoning history for this run
        save_reasoning_history(final_state)
        
        # Print output
        print("[Workflow] Final Answer:", final_state["final_answer"])
        print("[Workflow] Tool Output:", final_state["tool_output"])
        print("[Workflow] Reasoning Steps:")
        for step in final_state["reasoning_steps"]:
            print("-", step)
        print("\n---\n")

if __name__ == "__main__":
    main()
