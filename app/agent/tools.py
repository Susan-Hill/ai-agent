def calculator(expression: str) -> str:
    # Evaluate a simple math expression
    try:
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return f"Calculator error: {e}"


def read_file(path: str) -> str:
    # Read a text file from disk
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"File read error: {e}"