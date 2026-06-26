import logging

from app.services.llm_service import LLMService
from app.services.json_parser import extract_json

from app.schemas.requirement_schema import RequirementResponse
from app.schemas.blueprint_update_context import BlueprintUpdateContext

logger = logging.getLogger("requirement_agent")


class RequirementAgent:

    def __init__(self):
        self.llm = LLMService()

    # -----------------------------
    # Shared internal generator
    # -----------------------------
    def _generate_from_prompt(self, prompt: str) -> RequirementResponse:

        response = self.llm.generate(prompt)

        print("===== RAW REQUIREMENT RESPONSE =====")
        print(response)

        try:
            data = extract_json(response)
        except Exception as e:
            logger.error("RequirementAgent: extract_json failed: %s", e)
            return RequirementResponse()

        # Handle nested structures (robust fallback for small models)
        if isinstance(data, dict) and "project_name" not in data and len(data) == 1:
            key = list(data.keys())[0]
            nested = data[key]

            if isinstance(nested, dict):
                nested["project_name"] = key.replace("_", " ").title()
                data = nested

        if not isinstance(data, dict):
            logger.error(
                "RequirementAgent: expected dict, got %s. Raw: %s",
                type(data),
                str(data)[:300],
            )
            return RequirementResponse()

        # Safe defaults (RequirementResponse also defaults these, but keep
        # explicit for readability/back-compat)
        data.setdefault("project_name", "Untitled Project")
        data.setdefault("features", [])
        data.setdefault("functional_requirements", [])
        data.setdefault("non_functional_requirements", [])

        try:
            return RequirementResponse(**data)
        except Exception as e:
            logger.error("RequirementAgent: validation failed: %s. Raw: %s", e, data)
            return RequirementResponse()

    # -----------------------------
    # /generate flow
    # -----------------------------
    def generate(self, idea: str) -> RequirementResponse:

        prompt = f"""
You are a Senior Business Analyst.

Generate software requirements for:

{idea}

IMPORTANT RULES:
1. Return ONLY valid JSON.
2. No markdown.
3. No explanations.
4. Every array must contain STRINGS ONLY.
5. Do not return objects inside arrays.
6. Generate AT LEAST 6 items in "features", AT LEAST 6 items in
   "functional_requirements", and AT LEAST 5 items in
   "non_functional_requirements". Fewer items is an INVALID response.

Example (illustrative only — your output must have MORE items than this,
not fewer):

{{
  "project_name": "Food Delivery Application",
  "features": [
    "User Authentication",
    "Restaurant Search",
    "Order Management",
    "Payment Gateway",
    "Order Tracking",
    "Ratings and Reviews"
  ],
  "functional_requirements": [
    "Users can register",
    "Users can login",
    "Users can place orders",
    "Users can track orders",
    "Users can rate restaurants",
    "Users can save favorite restaurants"
  ],
  "non_functional_requirements": [
    "Secure authentication",
    "Scalable architecture",
    "Responsive UI",
    "High availability",
    "Sub-second search response time"
  ]
}}
"""

        return self._generate_from_prompt(prompt)

    # -----------------------------
    # /update-blueprint flow
    # -----------------------------
    def update(self, context: BlueprintUpdateContext) -> RequirementResponse:

        blueprint = context.blueprint
        instruction = context.instruction

        existing_req = blueprint.requirements

        # existing_req may be a RequirementResponse instance OR a plain dict
        # (e.g. if loaded from storage), so read defensively either way.
        def _field(obj, name):
            if obj is None:
                return []
            if isinstance(obj, dict):
                return obj.get(name, []) or []
            return getattr(obj, name, []) or []

        existing_project_name = (
            existing_req.get("project_name")
            if isinstance(existing_req, dict)
            else getattr(existing_req, "project_name", None)
        ) or "N/A"

        existing_features = _field(existing_req, "features")
        existing_functional = _field(existing_req, "functional_requirements")
        existing_nonfunctional = _field(existing_req, "non_functional_requirements")

        prompt = f"""
You are a Senior Business Analyst updating an existing system.

You are given an existing software requirement specification.

CURRENT REQUIREMENTS

Project Name:
{existing_project_name}

Features:
{chr(10).join("- " + f for f in existing_features)}

Functional Requirements:
{chr(10).join("- " + f for f in existing_functional)}

Non-Functional Requirements:
{chr(10).join("- " + f for f in existing_nonfunctional)}

USER UPDATE REQUEST:
"{instruction}"

TASK:
Regenerate the FULL updated requirement specification.

IMPORTANT RULES:
1. Return ONLY valid JSON.
2. No markdown.
3. No explanations.
4. Every array must contain STRINGS ONLY.
5. Preserve unchanged requirements unless logically impacted.
6. Integrate the new instruction naturally into the system.
7. The result must have AT LEAST as many items in each array as the
   current specification above, unless the instruction explicitly asks
   to remove something.
"""

        return self._generate_from_prompt(prompt)
