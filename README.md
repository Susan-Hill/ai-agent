# Tool-Using AI Agent — Version 1

## Objective
Version 1 focuses on building a minimal but complete autonomous agent that:
- Plans multi-step tasks
- Selects appropriate tools
- Executes tools safely
- Tracks intermediate state
- Produces a final response

This version prioritizes clarity, determinism, and correctness over feature breadth.

## Agent Responsibilities (V1)
1. Accept a user task
2. Determine whether tools are required
3. Select the appropriate tool
4. Execute the tool
5. Update internal state
6. Generate a final response

## Tools (V1)
- Calculator tool
- File reader tool
- Shell command tool (sandboxed)

## Architecture
The agent is implemented as a LangGraph state machine.

Nodes:
- Planner node
- Tool selection node
- Tool execution node
- State update node
- Final response node

State is explicitly passed between nodes to avoid uncontrolled autonomous loops.

## Project Structure
```
app/
├── main.py # Application entry point
├── agent/
│ ├── graph.py # LangGraph definition
│ ├── state.py # Agent state schema
│ ├── tools.py # Tool implementations
│ └── planner.py # Reasoning and planning logic
├── config.py
docker/
├── Dockerfile
docker-compose.yml
requirements.txt
README.md
.gitignore
```

## Development Environment
This project is fully containerized using Docker and Docker Compose.

### Build and Run
```bash
docker-compose build
docker-compose up
```
## Design Principles

- Deterministic agent execution

- Explicit tool permissions

- Clear reasoning boundaries

- No hidden autonomy

## Status

In progress — implementing core agent loop and tools