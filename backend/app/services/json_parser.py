import json
import re


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON found")

    json_text = match.group()

    # Remove trailing commas before } or ]
    json_text = re.sub(
        r",(\s*[}\]])",
        r"\1",
        json_text,
    )

    return json.loads(json_text)
