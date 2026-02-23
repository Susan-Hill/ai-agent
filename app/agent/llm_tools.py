import os
import requests
import json
import re

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

# Extract JSON snippet from LLM output
def extract_json(text: str):
    """
    Extract JSON snippet from LLM output.
    Returns dict if successful, else None.
    Handles extra markdown, code fences, or explanations.
    """
    # Remove any code fences first
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # Remove any leading/trailing whitespace
    text = text.strip()

    # Try to parse the whole text
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse JSON: {e}")
        pass

    # Fallback: search for the first {...} block in the text
    match = re.search(r"(\{.*?\})", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON in fallback: {e}")
            return None

    # If no JSON found
    return None

def call_ollama(prompt: str):
    url = f"{OLLAMA_BASE_URL}/v1/completions"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "max_tokens": 100,
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["text"]
    except Exception as e:
        logger.error(f"OLLAMA API call failed: {e}")
        raise