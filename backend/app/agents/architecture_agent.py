import logging

from app.services.llm_service import LLMService
from app.services.json_parser import extract_json
from app.services.safe_llm import SafeLLM

from app.schemas.requirement_schema import RequirementResponse
from app.schemas.architecture_schema import ArchitectureResponse

logger = logging.getLogger("architecture_agent")

LIST_FIELDS = [
    "frontend",
    "backend",
    "database",
    "authentication",
    "services",
    "deployment",
]


class ArchitectureAgent:

    def __init__(self):
        self.llm = LLMService()

    def _parse(self, response: str) -> dict:

        print("===== RAW ARCHITECTURE RESPONSE =====")
        print(response)

        data = extract_json(response)

        if not isinstance(data, dict):
            logger.error(
                "ArchitectureAgent: expected dict, got %s. Raw: %s",
                type(data),
                str(data)[:300],
            )
            return {}

        data.setdefault("architecture_type", "Microservices")

        for field in LIST_FIELDS:
            data[field] = SafeLLM.ensure_string_list(data.get(field))

        # additional_features is a list of {name, details} objects, not
        # plain strings, so it does NOT go through ensure_string_list.
        # The schema's own validator handles malformed entries; just make
        # sure we pass through a list (not None) so Pydantic sees an
        # empty default rather than erroring on a missing key.
        data.setdefault("additional_features", data.get("additional_features", []))

        return data

    def generate(self, requirements: RequirementResponse) -> ArchitectureResponse:

        prompt = f"""
You are a Senior Software Architect.

Project:
{requirements.project_name}

Features:
{chr(10).join("- " + f for f in requirements.features)}

Functional Requirements:
{chr(10).join("- " + f for f in requirements.functional_requirements)}

Non Functional Requirements:
{chr(10).join("- " + f for f in requirements.non_functional_requirements)}

STRICT JSON ONLY. Every list below must contain real, specific values, not
placeholders. "additional_features" must contain AT LEAST 3 items that map
directly to the project's features above (e.g. if a feature is "Search
Functionality", describe HOW it's architected).

{{
  "architecture_type": "Microservices",
  "frontend": ["React"],
  "backend": ["Node.js", "Express"],
  "database": ["PostgreSQL"],
  "authentication": ["JWT"],
  "services": ["API Gateway", "Notification Service"],
  "deployment": ["Docker", "AWS ECS"],
  "additional_features": [
    {{
      "name": "Search Functionality with Autocomplete",
      "details": "Uses Elasticsearch for indexing and real-time autocomplete suggestions"
    }},
    {{
      "name": "Social Media Integration",
      "details": "OAuth-based login via Google and Facebook using Passport.js"
    }}
  ]
}}
"""

        response = self.llm.generate(prompt)

        try:
            data = self._parse(response)
            return ArchitectureResponse(**data)
        except Exception as e:
            logger.error("ArchitectureAgent: failed to build response: %s", e)
            return ArchitectureResponse()
