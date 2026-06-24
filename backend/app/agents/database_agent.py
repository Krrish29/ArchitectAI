from app.services.llm_service import LLMService
from app.services.json_parser import extract_json
from app.schemas.requirement_schema import RequirementResponse
from app.schemas.database_schema import DatabaseResponse


class DatabaseAgent:

    def __init__(self):
        self.llm = LLMService()

    def generate(
        self,
        requirements: RequirementResponse,
    ) -> DatabaseResponse:

        prompt = f"""
You are a Senior Database Architect.

Project Name:
{requirements.project_name}

Features:
{chr(10).join("- " + f for f in requirements.features)}

Functional Requirements:
{chr(10).join("- " + f for f in requirements.functional_requirements)}

Design a production-ready database schema.

IMPORTANT RULES:
1. Return ONLY valid JSON.
2. No markdown.
3. No explanations.
4. No comments.
5. No trailing commas.
6. Every array must contain STRINGS ONLY.
7. Entities should represent real database tables.
8. Relationships must use natural language.
9. Indexes must use table.column notation.

Example:

{{
  "database": "PostgreSQL",
  "entities": [
    "Users",
    "Movies",
    "Subscriptions",
    "WatchHistory",
    "Payments"
  ],
  "relationships": [
    "User has one Subscription",
    "User has many WatchHistory records",
    "Movie has many WatchHistory records"
  ],
  "indexes": [
    "users.email",
    "movies.title",
    "watch_history.user_id"
  ]
}}

Return this exact schema:

{{
  "database": "string",
  "entities": [
    "string"
  ],
  "relationships": [
    "string"
  ],
  "indexes": [
    "string"
  ]
}}

Generate meaningful entities,
relationships and indexes.
"""

        response = self.llm.generate(prompt)

        print("===== RAW DATABASE RESPONSE =====")
        print(response)

        try:
            data = extract_json(response)

        except Exception as e:
            print("===== DATABASE PARSE ERROR =====")
            print(e)

            print("===== RAW DATABASE RESPONSE =====")
            print(response)

            raise e

        print(f"[DatabaseAgent] Project: " f"{requirements.project_name}")

        print(f"[DatabaseAgent] Database: " f"{data.get('database', 'Unknown')}")

        print(
            f"[DatabaseAgent] Entities Generated: " f"{len(data.get('entities', []))}"
        )

        print(
            f"[DatabaseAgent] Relationships Generated: "
            f"{len(data.get('relationships', []))}"
        )

        print(f"[DatabaseAgent] Indexes Generated: " f"{len(data.get('indexes', []))}")

        return DatabaseResponse(**data)
