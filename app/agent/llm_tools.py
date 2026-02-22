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
    """
    # Look for JSON inside ``` ... ``` 
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    # fallback: try to parse the whole string
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None

def call_ollama(prompt: str):
    url = f"{OLLAMA_BASE_URL}/v1/completions"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "max_tokens": 100,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    #print("[DEBUG] LLM response:", response.text, flush=True)
    return response.json()["choices"][0]["text"]