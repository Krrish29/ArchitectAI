from app.services.llm_service import LLMService
from app.services.json_parser import extract_json

from app.schemas.requirement_schema import RequirementResponse
from app.schemas.architecture_schema import ArchitectureResponse
from app.schemas.database_schema import DatabaseResponse
from app.schemas.api_schema import ApiResponse


class ApiAgent:

    def __init__(self):
        self.llm = LLMService()

    def generate(
        self,
        requirements: RequirementResponse,
        architecture: ArchitectureResponse,
        database: DatabaseResponse,
    ) -> ApiResponse:

        prompt = f"""
You are a Senior Backend Architect.

Project Name:
{requirements.project_name}

Features:
{chr(10).join("- " + f for f in requirements.features)}

Database:
{database.database}

Entities:
{chr(10).join("- " + e for e in database.entities)}

Generate REST APIs.

IMPORTANT RULES:
1. Return ONLY valid JSON.
2. No markdown.
3. No explanations.
4. No comments.
5. No trailing commas.
6. Every array must contain STRINGS ONLY.

Example:

{{
  "endpoints": [
    "POST /auth/register",
    "POST /auth/login",
    "GET /movies",
    "POST /subscriptions"
  ],
  "request_schemas": [
    "LoginRequest",
    "RegisterRequest",
    "CreateSubscriptionRequest"
  ],
  "response_schemas": [
    "LoginResponse",
    "MovieResponse",
    "SubscriptionResponse"
  ]
}}

Return this exact schema:

{{
  "endpoints": ["string"],
  "request_schemas": ["string"],
  "response_schemas": ["string"]
}}
"""

        response = self.llm.generate(prompt)

        print("===== RAW API RESPONSE =====")
        print(response)

        data = extract_json(response)

        print(f"[ApiAgent] Project: " f"{requirements.project_name}")

        print(f"[ApiAgent] Endpoints Generated: " f"{len(data.get('endpoints', []))}")

        print(f"[ApiAgent] Request Schemas: " f"{len(data.get('request_schemas', []))}")

        print(
            f"[ApiAgent] Response Schemas: " f"{len(data.get('response_schemas', []))}"
        )

        return ApiResponse(**data)
