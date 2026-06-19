from app.services.llm_service import LLMService
from app.services.json_parser import extract_json
from app.schemas.requirement_schema import RequirementResponse


class RequirementAgent:

    def __init__(self):
        self.llm = LLMService()

    def normalize_list(self, items):
        result = []

        for item in items:
            if isinstance(item, str):
                result.append(item)

            elif isinstance(item, dict):
                result.append(
                    item.get("description")
                    or item.get("feature")
                    or item.get("requirement")
                    or str(item)
                )

        return result

    def generate(self, idea: str):

        prompt = f"""
You are a Senior Business Analyst.

Generate software requirements for:

{idea}

IMPORTANT RULES:
1. Return ONLY valid JSON.
2. Do not include markdown.
3. Do not include explanations.
4. Every array must contain STRINGS ONLY.
5. Do not return objects inside arrays.

Example:

{{
  "project_name": "Food Delivery Application",
  "features": [
    "User Authentication",
    "Restaurant Search",
    "Order Management",
    "Payment Gateway"
  ],
  "functional_requirements": [
    "Users can register",
    "Users can login",
    "Users can place orders",
    "Users can track orders"
  ],
  "non_functional_requirements": [
    "Secure authentication",
    "Scalable architecture",
    "Responsive UI",
    "High availability"
  ]
}}
"""

        response = self.llm.generate(prompt)

        data = extract_json(response)

        print(f"[RequirementAgent] Project: " f"{data.get('project_name', 'Unknown')}")
        print(
            f"[RequirementAgent] Features Identified: "
            f"{len(data.get('features', []))}"
        )
        print(
            f"[RequirementAgent] Functional Requirements: "
            f"{len(data.get('functional_requirements', []))}"
        )
        print(
            f"[RequirementAgent] Non Functional Requirements: "
            f"{len(data.get('non_functional_requirements', []))}"
        )

        data["features"] = self.normalize_list(data.get("features", []))

        data["functional_requirements"] = self.normalize_list(
            data.get("functional_requirements", [])
        )

        data["non_functional_requirements"] = self.normalize_list(
            data.get("non_functional_requirements", [])
        )

        return RequirementResponse(**data)
