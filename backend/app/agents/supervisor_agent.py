import json
import re
import logging

from app.services.llm_service import LLMService
from app.schemas.blueprint_update_context import BlueprintUpdateContext

logger = logging.getLogger("supervisor_agent")


class SupervisorAgent:

    # "requirement" removed from the *selectable* set — Workflow always
    # runs it regardless of what the supervisor picks, so asking the LLM
    # to choose it is a no-op that just adds noise to its decision.
    VALID_AGENTS = ["architecture", "database", "api", "planner"]

    # Used when supervisor fails completely — run everything
    DEFAULT_FALLBACK = ["architecture", "database", "api", "planner"]

    def __init__(self):
        self.llm = LLMService()

    # --------------------------------------------------
    # CORE JSON PARSER — greedy, nested-safe, never raises
    # --------------------------------------------------
    def safe_extract_json(self, text: str) -> dict | None:
        """
        Three-tier extraction. Returns None if all tiers fail.
        Never raises an exception.
        """

        # Strip markdown fences
        text = re.sub(r"```(?:json)?", "", text).strip()

        # Tier 1: direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Tier 2: greedy outermost {...} block, trailing-comma fix only
        # (NOTE: no whitespace-collapse here — that operation is blind to
        # string boundaries and isn't needed for json.loads to succeed)
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            cleaned = match.group()
            cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)  # trailing commas
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass

        # Tier 3: keyword scan — extract any agent names mentioned in free text.
        # NOTE: this is a substring match against the whole raw response, so
        # it can produce false positives if the model's prose happens to
        # mention an agent name without intending to select it (e.g. "this
        # project will need an API"). It's a last-resort recovery tier, kept
        # because a plausible guess beats a hard failure, but treat any
        # result that came from this tier as lower-confidence than Tiers 1/2.
        found_agents = [a for a in self.VALID_AGENTS if a in text.lower()]
        if found_agents:
            logger.warning(
                "SupervisorAgent: Tier 3 keyword rescue used (low confidence): %s",
                found_agents,
            )
            return {
                "selected_agents": found_agents,
                "reasoning": {"note": "recovered_via_keyword_scan"},
            }

        return None  # complete failure

    # --------------------------------------------------
    # VALIDATE + NORMALISE supervisor dict
    # --------------------------------------------------
    def _normalise(self, data: dict) -> dict:
        """
        Ensures selected_agents is a non-empty list of valid agent names.
        Returns normalised dict or raises ValueError if unfixable.
        """

        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data)}")

        agents = data.get("selected_agents", [])

        # Handle case where LLM returns a dict instead of list
        if isinstance(agents, dict):
            agents = list(agents.keys())

        # Handle comma-separated string  e.g. "api, database, planner"
        if isinstance(agents, str):
            agents = [a.strip() for a in agents.split(",")]

        if not isinstance(agents, list):
            agents = []

        # Filter to known valid agents only
        agents = [
            a.strip().lower()
            for a in agents
            if isinstance(a, str) and a.strip().lower() in self.VALID_AGENTS
        ]
        # de-duplicate while preserving order
        agents = list(dict.fromkeys(agents))

        if not agents:
            raise ValueError("No valid agents after normalisation")

        reasoning = data.get("reasoning", {})
        if not isinstance(reasoning, dict):
            reasoning = {}

        return {"selected_agents": agents, "reasoning": reasoning}

    # --------------------------------------------------
    # DECIDE  (generation flow)
    # --------------------------------------------------
    def decide(self, idea: str) -> dict:

        prompt = f"""You are an AI Engineering Manager deciding which agents to run.

AVAILABLE AGENTS:
- architecture
- database
- api
- planner

(Note: requirements are always generated separately and do not need to be selected.)

PROJECT IDEA: "{idea}"

CRITICAL RULES:
- Return ONLY a JSON object
- No markdown, no backticks, no explanation
- Output must start with {{ and end with }}
- selected_agents must include at least one agent

REQUIRED FORMAT:
{{
  "selected_agents": ["architecture", "database", "api", "planner"],
  "reasoning": {{
    "architecture": "reason here",
    "database": "reason here"
  }}
}}"""

        result = self._run_supervisor(prompt, label=idea, flow="decide")
        self._print_summary(idea, result)
        return result

    # --------------------------------------------------
    # ANALYZE_UPDATE  (update flow)
    # --------------------------------------------------
    def analyze_update(self, context: BlueprintUpdateContext) -> dict:

        prompt = f"""You are an AI Software Architect deciding which parts to regenerate.

AVAILABLE AGENTS:
- architecture
- database
- api
- planner

(Note: requirements are always regenerated separately and do not need to be selected.)

USER INSTRUCTION: "{context.instruction}"

CRITICAL RULES:
- Return ONLY a JSON object
- No markdown, no backticks, no explanation

REQUIRED FORMAT:
{{
  "selected_agents": ["api", "planner"],
  "reasoning": {{
    "api": "user changed endpoints",
    "planner": "timeline needs update"
  }}
}}"""

        return self._run_supervisor(prompt, label=context.instruction, flow="update")

    # --------------------------------------------------
    # SHARED INTERNAL RUNNER
    # --------------------------------------------------
    def _run_supervisor(self, prompt: str, label: str, flow: str) -> dict:
        """
        Calls LLM, parses, normalises, and falls back gracefully.
        NEVER raises — always returns a valid dict.
        """

        try:
            raw = self.llm.generate(prompt)
            print(f"===== RAW SUPERVISOR [{flow.upper()}] ({label}) =====")
            print(raw)

            data = self.safe_extract_json(raw)

            if data is None:
                raise ValueError("All JSON extraction tiers failed")

            return self._normalise(data)

        except Exception as e:
            logger.warning(
                "SupervisorAgent [%s] failed (%s), using default agents: %s",
                flow,
                e,
                self.DEFAULT_FALLBACK,
            )

            return {
                "selected_agents": self.DEFAULT_FALLBACK,
                "reasoning": {
                    "fallback": f"Supervisor failed ({e}), running default agents"
                },
            }

    # --------------------------------------------------
    # PRETTY PRINT
    # --------------------------------------------------
    def _print_summary(self, idea: str, result: dict):
        print("\n" + "=" * 60)
        print("ARCHITECTAI :: SUPERVISOR AGENT")
        print("=" * 60)
        print(f"\nPROJECT: {idea}\n")
        print("SELECTED AGENTS:")
        for agent in result["selected_agents"]:
            print(f"  - {agent}")
            reason = result["reasoning"].get(agent)
            if reason:
                print(f"    -> {reason}")
        print("=" * 60)
