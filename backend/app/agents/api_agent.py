import logging

from app.services.llm_service import LLMService
from app.services.json_parser import extract_json

from app.schemas.api_schema import ApiResponse

logger = logging.getLogger("api_agent")


def _read_field(obj, name, default):
    """Read a field off an object whether it's a Pydantic model or a dict."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _entity_summary(entities):
    """Render entities (list of dicts or strings) into a short, clean prompt-friendly list."""
    lines = []
    for e in entities or []:
        if isinstance(e, dict):
            name = e.get("name", "Entity")
            desc = e.get("description", "")
            lines.append(f"{name}" + (f" — {desc}" if desc else ""))
        else:
            lines.append(str(e))
    return lines


class ApiAgent:

    def __init__(self):
        self.llm = LLMService()

    def _parse(self, response: str) -> ApiResponse:

        print("===== RAW API RESPONSE =====")
        print(response)

        data = extract_json(response)

        if not isinstance(data, dict):
            logger.error(
                "ApiAgent: expected dict, got %s. Raw: %s",
                type(data),
                str(data)[:300],
            )
            data = {}

        # Safe defaults for optional fields the LLM often omits
        data.setdefault("base_url", "/api")
        data.setdefault("endpoints", [])
        data.setdefault("request_schemas", [])
        data.setdefault("response_schemas", [])

        return ApiResponse(**data)

    def generate(self, req, db) -> ApiResponse:

        # FIXED: previously this always evaluated to "unknown" / [] for the
        # normal case (db as a DatabaseResponse object), because the
        # isinstance(db, dict) check gated the WHOLE expression rather than
        # just the dict-access branch. getattr() works on both objects and
        # dicts (dicts just don't have a .database attribute, so it falls
        # through to None) — so reading via getattr first, with a dict-get
        # fallback, is the safe order for either type.
        db_name = _read_field(db, "database", "unknown")
        entities = _read_field(db, "entities", [])

        project = getattr(req, "project_name", None) or "the project"
        entity_lines = _entity_summary(entities)

        prompt = f"""You are a Senior API Architect.

Project: {project}
Database: {db_name}

Entities:
{chr(10).join("- " + e for e in entity_lines) if entity_lines else "- (none specified)"}

Generate a complete REST API design that covers CRUD operations for EVERY
entity listed above, plus any auth/utility endpoints the project needs.

RULES:
- Return ONLY a JSON object
- No markdown, no backticks, no explanation
- Generate AT LEAST 2 endpoints per entity listed above (e.g. list + create,
  or list + create + update + delete for entities the user can manage)
- Fewer endpoints, or endpoints unrelated to the entities above, is an
  INVALID response

REQUIRED FORMAT (illustrative only — your output must cover ALL entities,
not just User):
{{
  "base_url": "/api",
  "endpoints": [
    {{
      "method": "GET",
      "path": "/users",
      "description": "Get all users",
      "request_body": null,
      "response": {{"data": "array of user objects"}}
    }},
    {{
      "method": "POST",
      "path": "/users",
      "description": "Create a new user",
      "request_body": {{"name": "string", "email": "string"}},
      "response": {{"data": "created user object"}}
    }}
  ],
  "request_schemas": [],
  "response_schemas": []
}}"""

        response = self.llm.generate(prompt)

        try:
            return self._parse(response)
        except Exception as e:
            logger.error("ApiAgent: parse failed: %s", e)
            return ApiResponse(
                base_url="/api",
                endpoints=[],
                request_schemas=[],
                response_schemas=[],
            )
