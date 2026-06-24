from app.services.llm_service import LLMService
from app.schemas.requirement_schema import RequirementResponse
from app.schemas.architecture_schema import ArchitectureResponse
from app.schemas.planner_schema import PlannerResponse
from app.services.json_parser import extract_json


class PlannerAgent:

    def __init__(self):
        self.llm = LLMService()

    def generate(
        self,
        requirements: RequirementResponse,
        architecture: ArchitectureResponse,
    ) -> PlannerResponse:

        prompt = f"""
You are a senior engineering manager.

Project Name:
{requirements.project_name}

Features:
{chr(10).join("- " + f for f in requirements.features)}

Architecture Type:
{architecture.architecture_type}

Frontend:
{chr(10).join("- " + f for f in architecture.frontend)}

Backend:
{chr(10).join("- " + f for f in architecture.backend)}

Database:
{chr(10).join("- " + f for f in architecture.database)}

Services:
{chr(10).join("- " + f for f in architecture.services)}

Create an implementation roadmap.

Break the project into logical phases.

Return ONLY valid JSON.

Rules:
1. Return JSON only.
2. No markdown.
3. No explanations.
4. No comments.
5. No trailing commas.
6. Response must be parseable by Python json.loads().

Return this exact schema:

{{
  "phases": [
    {{
      "phase_name": "string",
      "tasks": ["string"]
    }}
  ]
}}

Every phase must contain meaningful tasks.
Do not return empty values.
"""

        response = self.llm.generate(prompt)

        print("===== RAW PLANNER RESPONSE =====")
        print(response)

        try:
            data = extract_json(response)
        except Exception as e:
            print("===== PLANNER PARSE ERROR =====")
            print(e)

            print("===== RAW PLANNER RESPONSE =====")
            print(response)

            raise e

        print("===== PARSED PLANNER DATA =====")
        print(data)

        print(f"[PlannerAgent] Project: " f"{requirements.project_name}")

        print(f"[PlannerAgent] Architecture: " f"{architecture.architecture_type}")

        print(
            f"[PlannerAgent] Total Phases Generated: " f"{len(data.get('phases', []))}"
        )

        for index, phase in enumerate(
            data.get("phases", []),
            start=1,
        ):
            print(
                f"[PlannerAgent] "
                f"Phase {index}: "
                f"{phase.get('phase_name', 'Unknown')} "
                f"({len(phase.get('tasks', []))} tasks)"
            )

        return PlannerResponse(**data)
