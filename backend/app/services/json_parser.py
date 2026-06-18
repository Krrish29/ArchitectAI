import json
import re


def extract_json(text: str):
    """
    Extracts the first JSON object from an LLM response.
    """

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in response.")

    json_text = match.group()

    return json.loads(json_text)