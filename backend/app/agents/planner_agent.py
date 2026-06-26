from app.services.llm_service import LLMService
from app.services.json_parser import extract_json
from app.schemas.planner_schema import PlannerResponse


class PlannerAgent:

    def __init__(self):
        self.llm = LLMService()

    # -----------------------------
    # NORMALIZER (CRITICAL FIX)
    # -----------------------------
    def _normalize(self, data: dict) -> dict:

        # -------------------------
        # FIX PHASES
        # -------------------------
        fixed_phases = []

        for p in data.get("phases", []) or []:
            if isinstance(p, str):
                fixed_phases.append(
                    {
                        "phase_name": p,
                        "tasks": [],
                        "dependencies": [],
                        "estimated_duration_days": 7,
                    }
                )
            elif isinstance(p, dict):
                fixed_phases.append(
                    {
                        "phase_name": p.get("phase_name") or p.get("name") or "Phase",
                        "tasks": p.get("tasks", []) or [],
                        "dependencies": p.get("dependencies", []) or [],
                        "estimated_duration_days": p.get("estimated_duration_days", 7),
                    }
                )
            # silently skip anything that's neither str nor dict (e.g. None, int)

        data["phases"] = fixed_phases

        # -------------------------
        # FIX MILESTONES
        # -------------------------
        fixed_milestones = []

        for m in data.get("milestones", []) or []:
            if isinstance(m, str):
                fixed_milestones.append({"name": m, "description": ""})
            elif isinstance(m, dict):
                fixed_milestones.append(
                    {
                        "name": m.get("name", "Milestone"),
                        "description": m.get("description", ""),
                    }
                )

        data["milestones"] = fixed_milestones

        # -------------------------
        # DEFAULT TIMELINE
        # -------------------------
        data.setdefault("timeline", "4-6 weeks")

        return data

    # -----------------------------
    # PARSE SAFE
    # -----------------------------
    def _parse(self, response: str) -> PlannerResponse:

        print("===== RAW PLANNER RESPONSE =====")
        print(response)

        data = extract_json(response)

        # 🔥 CRITICAL FIX
        data = self._normalize(data)

        return PlannerResponse(**data)

    # -----------------------------
    # GENERATE
    # -----------------------------
    def generate(self, req, db, api) -> PlannerResponse:

        project = getattr(req, "project_name", None) or (
            req.get("project_name", "Project") if isinstance(req, dict) else "Project"
        )

        endpoint_count = 0
        if hasattr(api, "endpoints"):
            endpoint_count = len(api.endpoints)
        elif isinstance(api, dict):
            endpoint_count = len(api.get("endpoints", []))

        prompt = f"""
You are a Senior Project Manager creating a detailed implementation roadmap.

Return ONLY valid JSON.

YOU MUST FOLLOW THIS EXACT SCHEMA:

{{
  "phases": [
    {{
      "phase_name": "string",
      "tasks": ["task description 1", "task description 2", "task description 3"],
      "dependencies": [],
      "estimated_duration_days": 7
    }}
  ],
  "timeline": "4-6 weeks",
  "milestones": [
    {{
      "name": "string",
      "description": "string"
    }}
  ]
}}

CRITICAL RULES (these are non-negotiable):
- Every phase MUST include a "tasks" array with AT LEAST 3 specific, concrete tasks.
- An empty or missing "tasks" array is an INVALID response and will be rejected.
- Each task must be a specific, actionable item (e.g. "Design the user authentication schema"), NOT a vague label.
- Generate exactly 4 to 6 phases covering the full project lifecycle (e.g. Planning, Design, Development, Testing, Deployment).
- NEVER use "name" for phases (ONLY phase_name).
- NO extra fields.
- NO markdown.
- NO explanation outside the JSON.

EXAMPLE of a correctly filled phase (for reference only, do not copy literally):
{{
  "phase_name": "Backend Setup",
  "tasks": [
    "Set up Node.js project structure and dependencies",
    "Configure PostgreSQL database connection",
    "Implement JWT authentication middleware",
    "Create base API routing structure"
  ],
  "dependencies": [],
  "estimated_duration_days": 7
}}

PROJECT: {project}
API endpoints to implement: {endpoint_count}
"""

        response = self.llm.generate(prompt)

        try:
            return self._parse(response)
        except Exception as e:
            print("[PlannerAgent] Failed:", e)

            return PlannerResponse(phases=[], timeline="4-6 weeks", milestones=[])
