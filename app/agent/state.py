from typing import TypedDict, List, Optional


# Defines the structure of the agent's state throughout the workflow.
class AgentState(TypedDict):
    user_input: str

    # Planning
    plan: Optional[str]

    # Tool usage
    selected_tool: Optional[str]
    tool_input: Optional[str]
    tool_output: Optional[str]

    # Reasoning and traceability
    reasoning_steps: List[str]

    # Control
    step_count: int
    max_steps: int

    # Final output
    final_answer: Optional[str]