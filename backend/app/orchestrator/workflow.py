from copy import deepcopy

from app.agents.supervisor_agent import SupervisorAgent
from app.agents.requirement_agent import RequirementAgent
from app.agents.database_agent import DatabaseAgent
from app.agents.api_agent import ApiAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.architecture_agent import ArchitectureAgent

from app.schemas.final_response import FinalResponse
from app.schemas.requirement_schema import RequirementResponse
from app.schemas.blueprint_update_context import BlueprintUpdateContext

# Sentinel used when DatabaseAgent fails — prevents ApiAgent from crashing
_EMPTY_DB = {"entities": [], "relationships": [], "indexes": []}


class Workflow:

    def __init__(self):
        self.supervisor = SupervisorAgent()
        self.architecture_agent = ArchitectureAgent()
        self.requirement_agent = RequirementAgent()
        self.database_agent = DatabaseAgent()
        self.api_agent = ApiAgent()
        self.planner_agent = PlannerAgent()

    # --------------------------------------------------
    # EXECUTE  (generation flow)
    # --------------------------------------------------
    def execute(self, idea: str) -> FinalResponse:

        # Supervisor NEVER raises now — always returns valid dict
        supervisor_result = self.supervisor.decide(idea)
        selected = supervisor_result.get("selected_agents", [])
        reasoning = supervisor_result.get("reasoning", {})

        requirement = None
        architecture = None
        database = None
        api = None
        plan = None
        errors = {}

        # --- Requirement (always run, no guard needed) ---
        try:
            requirement = self.requirement_agent.generate(idea)
        except Exception as e:
            print(f"[Workflow] RequirementAgent failed: {e}")
            errors["requirement"] = str(e)
            # FIXED: previously fell back to a plain string here, which
            # FinalResponse.requirements (typed Optional[RequirementResponse])
            # would reject with a Pydantic ValidationError further down —
            # turning a handled agent failure into an unhandled crash one
            # step later. A real RequirementResponse instance keeps every
            # downstream agent (which reads requirement.project_name,
            # requirement.features, etc.) working normally.
            requirement = RequirementResponse(project_name=idea or "Untitled Project")

        # --- Architecture ---
        if "architecture" in selected:
            try:
                architecture = self.architecture_agent.generate(requirement)
            except Exception as e:
                print(f"[Workflow] ArchitectureAgent failed: {e}")
                errors["architecture"] = str(e)

        # --- Database ---
        if "database" in selected:
            try:
                database = self.database_agent.generate(requirement)
            except Exception as e:
                print(f"[Workflow] DatabaseAgent failed: {e}")
                errors["database"] = str(e)

        # --- API — safe db fallback prevents crash when database is None ---
        if "api" in selected:
            try:
                db_input = database if database is not None else _EMPTY_DB
                api = self.api_agent.generate(requirement, db_input)
            except Exception as e:
                print(f"[Workflow] ApiAgent failed: {e}")
                errors["api"] = str(e)

        # --- Planner — safe fallbacks for all deps ---
        if "planner" in selected:
            try:
                db_input = database if database is not None else _EMPTY_DB
                api_input = api if api is not None else {}
                plan = self.planner_agent.generate(requirement, db_input, api_input)
            except Exception as e:
                print(f"[Workflow] PlannerAgent failed: {e}")
                errors["planner"] = str(e)

        if errors:
            print(f"[Workflow] Completed with partial errors: {list(errors.keys())}")

        return FinalResponse(
            idea=idea,
            selected_agents=selected,
            reasoning=reasoning,
            requirements=requirement,
            architecture=architecture,
            database=database,
            api=api,
            plan=plan,
        )

    # --------------------------------------------------
    # UPDATE BLUEPRINT
    # --------------------------------------------------
    def update_blueprint(self, context: BlueprintUpdateContext) -> FinalResponse:

        blueprint = context.blueprint

        # Supervisor NEVER raises — safe fallback built in
        supervisor_result = self.supervisor.analyze_update(context)
        selected = supervisor_result.get("selected_agents", [])
        reasoning = supervisor_result.get("reasoning", {})

        updated = deepcopy(blueprint)

        # Requirement always regenerates on update
        try:
            requirement = self.requirement_agent.update(context)
            updated.requirements = requirement
        except Exception as e:
            print(f"[Workflow] RequirementAgent.update failed: {e}")
            requirement = blueprint.requirements  # keep existing
            updated.requirements = requirement

        # Preserve existing values as defaults
        architecture = blueprint.architecture
        database = blueprint.database
        api = blueprint.api
        plan = blueprint.plan

        if "architecture" in selected:
            try:
                architecture = self.architecture_agent.generate(requirement)
                updated.architecture = architecture
            except Exception as e:
                print(f"[Workflow] ArchitectureAgent update failed: {e}")

        if "database" in selected:
            try:
                database = self.database_agent.generate(requirement)
                updated.database = database
            except Exception as e:
                print(f"[Workflow] DatabaseAgent update failed: {e}")

        if "api" in selected:
            try:
                db_input = database if database is not None else _EMPTY_DB
                api = self.api_agent.generate(requirement, db_input)
                updated.api = api
            except Exception as e:
                print(f"[Workflow] ApiAgent update failed: {e}")

        if "planner" in selected:
            try:
                db_input = database if database is not None else _EMPTY_DB
                api_input = api if api is not None else {}
                plan = self.planner_agent.generate(requirement, db_input, api_input)
                updated.plan = plan
            except Exception as e:
                print(f"[Workflow] PlannerAgent update failed: {e}")

        return FinalResponse(
            idea=blueprint.idea,
            selected_agents=selected,
            reasoning=reasoning,
            requirements=updated.requirements,
            architecture=updated.architecture,
            database=updated.database,
            api=updated.api,
            plan=updated.plan,
        )
