import json
import re
import logging

logger = logging.getLogger("json_parser")

try:
    import json5  # forgiving JSON parser: handles trailing commas, comments, etc.

    _HAS_JSON5 = True
except ImportError:
    _HAS_JSON5 = False


def extract_json(text: str) -> dict:
    """
    Robust JSON extractor for LLM outputs.
    Handles nested JSON, trailing commas, extra prose, markdown fences.

    Strategy (in order, each step only runs if the previous one fails):
    1. Strip markdown fences, try strict json.loads on the whole text.
    2. Extract the outermost {...} block, try strict json.loads on that.
    3. If json5 is available, retry both of the above with json5.loads
       (tolerates trailing commas / comments WITHOUT mutating string content).
    4. Give up loudly, logging the raw text for debugging.

    NOTE: we deliberately do NOT run global regex replacements (e.g.
    collapsing whitespace, stripping trailing commas via regex) against
    the raw text. Those operations are blind to string boundaries and can
    silently corrupt array/string content (e.g. inside "tasks": [...]).
    json5 handles trailing commas correctly without touching string content.
    """

    original_text = text

    # Strip markdown code fences if present
    cleaned = re.sub(r"```(?:json)?", "", text).strip()

    # --- Attempt 1: strict parse of full cleaned text ---
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # --- Attempt 2: strict parse of the outermost {...} block ---
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    json_block = match.group() if match else None

    if json_block:
        try:
            return json.loads(json_block)
        except json.JSONDecodeError:
            pass

    # --- Attempt 3: forgiving parse with json5 (handles trailing commas,
    #     comments, unquoted keys) without doing blind regex surgery ---
    if _HAS_JSON5:
        for candidate in filter(None, [json_block, cleaned]):
            try:
                return json5.loads(candidate)
            except Exception:
                continue

    # --- All attempts failed: log full raw output and raise loudly ---
    logger.error(
        "extract_json: failed to parse LLM output. Raw text:\n%s",
        original_text,
    )
    raise ValueError(
        f"No valid JSON object could be extracted from LLM output.\n"
        f"Raw text (first 500 chars):\n{original_text[:500]}"
    )


class SafeLLM:

    @staticmethod
    def ensure_list(value):
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return value
        return [str(value)]

    @staticmethod
    def ensure_string_list(value):
        return [str(v) for v in SafeLLM.ensure_list(value)]
