# Tool-Using AI Agent (LangGraph)

## Overview
This project implements an autonomous, tool-using AI agent using LangChain and LangGraph.
The agent is designed to plan multi-step tasks, select and execute tools, and produce structured final responses using deterministic control flow.

The focus of this project is agent orchestration, tool execution, and system design, rather than prompt-only LLM usage.

## Why This Project
Modern AI systems require more than text generation.  
This project demonstrates:
- Autonomous decision-making
- Tool-based reasoning
- Explicit state management
- Controlled agent execution
- Observability and debugging through persistent logs and reasoning history

## Core Capabilities
- Multi-step reasoning
- Tool selection and execution
    - Calculator: supports +-*/ operations
    - Read File: read text files from disk
- Graph-based agent orchestration (LangGraph)
- Deterministic control flow
- Observability
    - Logging of all workflow steps
    - Reasoning history saved per run
- Edge case handling
    - Division by zero
    - Invalid tool inputs
- Containerized development environment with Docker and Docker Compose

## Architecture (High-Level)
1. User Input - typed into the console prompt
2. Planner - analyzes input, decides if a tool is needed
3. Tool Selection - uses LLM to select the appropriate tool and input
4. Tool Execution - executes the selected tool
5. State Update & Logging - updates agent state, logs actions
6. Final Response - returns the final result to the user
7. Reasoning History - saves JSON trace of the run for debugging or review

## Usage
Start the agent with Docker Compose:
```
docker compose run --rm agent
```
At the prompt, enter requests like:

### Calculator Examples

```
please calculate 5+5
please calculate 10-3
please calculate 7*8
please calculate 10/2
```
### Edge Cases
- Division by zero -> "Calculator error: division by zero"
- Invalid or no tool required -> "No tool was required"

## Observability & Logging
- Logs are saved to /logs/agent_YYYYMMDD_HHMMSS.log
- Reasoning history is saved per run in /logs/history as JSON files containing
    - user_input
    - selected_tool and tool_input
    - tool_output
    - final_answer
    - reasoning_steps

This enables debugging and review of agent reasoning after execution.

## Tech Stack
- Python
- LangGraph (for agent orchestration)
- Docker / Docker Compose
- Optional: LLM API (e.g. Ollama) for tool selection reasoning

## Project Status
Version 1 - Complete and stable

All core functionality implemented, including:
- Multi-step reasoning
- Tool execution
- Logging and reasoning history
- Edge case handling
- Containerized environment




