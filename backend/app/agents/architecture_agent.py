from app.services.llm_service import LLMService
from app.schemas.requirement_schema import RequirementResponse
from app.schemas.architecture_schema import ArchitectureResponse
from app.services.json_parser import extract_json


class ArchitectureAgent:

    def __init__(self):
        self.llm = LLMService()

    def generate(
        self,
        requirements: RequirementResponse,
    ) -> ArchitectureResponse:

        prompt = f"""
You are an expert software architect.

Project:
{requirements.project_name}

Features:
{chr(10).join("- " + f for f in requirements.features)}

Functional Requirements:
{chr(10).join("- " + f for f in requirements.functional_requirements)}

Non Functional Requirements:
{chr(10).join("- " + f for f in requirements.non_functional_requirements)}

Choose:
1. Architecture type
2. Frontend technologies
3. Backend technologies
4. Database technologies
5. Authentication mechanism
6. Important services
7. Deployment technologies

Return ONLY this JSON:

{{
  "architecture_type": "string",
  "frontend": ["string"],
  "backend": ["string"],
  "database": ["string"],
  "authentication": ["string"],
  "services": ["string"],
  "deployment": ["string"]
}}

Every field must contain meaningful values.
Never return empty strings or empty arrays.
"""

        response = self.llm.generate(prompt)

        data = extract_json(response)

        list_fields = [
            "frontend",
            "backend",
            "database",
            "authentication",
            "services",
            "deployment",
        ]

        for field in list_fields:
            value = data.get(field, [])

            if isinstance(value, str):
                value = [value]

            data[field] = value

        print(f"[ArchitectureAgent] Project: " f"{requirements.project_name}")
        print(
            f"[ArchitectureAgent] Architecture Type: "
            f"{data.get('architecture_type', 'Unknown')}"
        )
        print(
            f"[ArchitectureAgent] Frontend Stack: "
            f"{', '.join(data.get('frontend', []))}"
        )
        print(
            f"[ArchitectureAgent] Backend Stack: "
            f"{', '.join(data.get('backend', []))}"
        )
        print(
            f"[ArchitectureAgent] Database: " f"{', '.join(data.get('database', []))}"
        )

        return ArchitectureResponse(**data)
