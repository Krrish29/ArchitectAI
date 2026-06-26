import logging

from app.services.llm_service import LLMService
from app.services.json_parser import extract_json
from app.services.safe_llm import SafeLLM

from app.schemas.requirement_schema import RequirementResponse
from app.schemas.database_schema import DatabaseResponse
from app.schemas.blueprint_update_context import BlueprintUpdateContext

logger = logging.getLogger("database_agent")


class DatabaseAgent:

    def __init__(self):
        self.llm = LLMService()

    def _parse(self, response: str) -> dict:

        print("===== RAW DATABASE RESPONSE =====")
        print(response)

        data = extract_json(response)

        if not isinstance(data, dict):
            logger.error(
                "DatabaseAgent: expected dict, got %s. Raw: %s",
                type(data),
                str(data)[:300],
            )
            return {}

        data.setdefault("database", "PostgreSQL")

        # entities is now a list of {name, type, description} objects (or
        # plain strings, which the schema's validator will wrap). Do NOT
        # run it through ensure_string_list, since that would stringify
        # any dict entries into garbage text.
        data.setdefault("entities", data.get("entities", []))

        data["relationships"] = SafeLLM.ensure_string_list(data.get("relationships"))
        data["indexes"] = SafeLLM.ensure_string_list(data.get("indexes"))

        return data

    def _safe_build(self, response: str) -> DatabaseResponse:
        try:
            data = self._parse(response)
            return DatabaseResponse(**data)
        except Exception as e:
            logger.error("DatabaseAgent: failed to build response: %s", e)
            return DatabaseResponse()

    @staticmethod
    def _existing_field(blueprint_db, name, default):
        """Read a field off blueprint.database whether it's a model or a dict."""
        if blueprint_db is None:
            return default
        if isinstance(blueprint_db, dict):
            return blueprint_db.get(name, default)
        return getattr(blueprint_db, name, default)

    # -----------------------------
    # GENERATE
    # -----------------------------
    def generate(self, requirements: RequirementResponse) -> DatabaseResponse:

        prompt = f"""
You are a Senior Database Architect.

Project:
{requirements.project_name}

Features:
{chr(10).join("- " + f for f in requirements.features)}

Functional Requirements:
{chr(10).join("- " + f for f in requirements.functional_requirements)}

IMPORTANT RULES:
- Return ONLY valid JSON
- No explanations
- "entities" must be OBJECTS with name, type, and description (NOT plain strings)
- Generate AT LEAST 5 entities, AT LEAST 4 relationships, AT LEAST 3 indexes
- Fewer items, or plain-string entities, is an INVALID response

STRICT FORMAT (illustrative — your output must have MORE items than this):

{{
  "database": "PostgreSQL",
  "entities": [
    {{
      "name": "User",
      "type": "table",
      "description": "Stores user account and profile information"
    }},
    {{
      "name": "Movie",
      "type": "table",
      "description": "Stores movie metadata and catalog information"
    }}
  ],
  "relationships": [
    "User has many Movies through Watchlist",
    "User has one Profile"
  ],
  "indexes": [
    "User.email (unique)",
    "Movie.title"
  ]
}}
"""

        response = self.llm.generate(prompt)
        return self._safe_build(response)

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update(self, context: BlueprintUpdateContext) -> DatabaseResponse:

        b = context.blueprint

        project_name = self._existing_field(
            getattr(b, "requirements", None), "project_name", "N/A"
        )
        existing_db = self._existing_field(b.database, "database", "N/A")
        existing_entities = self._existing_field(b.database, "entities", [])
        existing_relationships = self._existing_field(b.database, "relationships", [])
        existing_indexes = self._existing_field(b.database, "indexes", [])

        def _entity_line(e):
            if isinstance(e, dict):
                return e.get("name", "Entity")
            return getattr(e, "name", str(e))

        prompt = f"""
You are updating an existing database design.

PROJECT:
{project_name}

EXISTING DATABASE ENGINE:
{existing_db}

EXISTING ENTITIES:
{chr(10).join("- " + _entity_line(e) for e in existing_entities) or "- (none yet)"}

EXISTING RELATIONSHIPS:
{chr(10).join("- " + r for r in existing_relationships) or "- (none yet)"}

EXISTING INDEXES:
{chr(10).join("- " + i for i in existing_indexes) or "- (none yet)"}

USER REQUEST:
{context.instruction}

TASK:
Regenerate the FULL updated database design, preserving existing entities,
relationships, and indexes unless the user request logically requires a
change.

IMPORTANT RULES:
- Return ONLY valid JSON
- No explanations
- "entities" must be OBJECTS with name, type, and description (NOT plain strings)
- The result must have AT LEAST as many entities/relationships/indexes as
  listed above, unless the instruction explicitly asks to remove something

STRICT FORMAT:

{{
  "database": "PostgreSQL",
  "entities": [
    {{"name": "User", "type": "table", "description": "..."}}
  ],
  "relationships": ["User has many Movies"],
  "indexes": ["User.email (unique)"]
}}
"""

        response = self.llm.generate(prompt)
        return self._safe_build(response)
