from copy import deepcopy
from typing import Callable, Optional

from app.agents.supervisor_agent import SupervisorAgent
from app.agents.requirement_agent import RequirementAgent
from app.agents.database_agent import DatabaseAgent
from app.agents.api_agent import ApiAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.architecture_agent import ArchitectureAgent
from app.orchestrator.agent_messages import AGENT_MESSAGES
from app.orchestrator.dependency_resolver import resolve_execution_plan
from app.orchestrator.event_dispatcher import EventDispatcher
from app.orchestrator.event_emitter import WorkflowEventEmitter
from app.schemas.stream_event import StreamEvent

from app.schemas.final_response import FinalResponse
from app.schemas.requirement_schema import RequirementResponse
from app.schemas.blueprint_update_context import BlueprintUpdateContext

# Sentinel used when DatabaseAgent fails — prevents ApiAgent from crashing
_EMPTY_DB = {"entities": [], "relationships": [], "indexes": []}


class Workflow:

    def __init__(self, event_callback: Optional[Callable] = None):
        self.supervisor = SupervisorAgent()
        self.architecture_agent = ArchitectureAgent()
        self.requirement_agent = RequirementAgent()
        self.database_agent = DatabaseAgent()
        self.api_agent = ApiAgent()
        self.planner_agent = PlannerAgent()
        self.event_callback = event_callback
        self.event_dispatcher: Optional[EventDispatcher] = None
        self.event_emitter: Optional[WorkflowEventEmitter] = None

    def _setup_event_pipeline(self):
        self.event_dispatcher = EventDispatcher(callback=self.event_callback)
        self.event_emitter = WorkflowEventEmitter(
            callback=self.event_dispatcher.dispatch
        )

    def _emit_agent_event(self, agent: str, status: str, message: str | None = None):
        if message is None:
            message = AGENT_MESSAGES.get(agent, {}).get(status, "")
        assert self.event_emitter is not None
        self.event_emitter.emit(agent=agent, status=status, message=message)

    def get_events(self) -> list[StreamEvent]:
        if self.event_dispatcher is None:
            return []
        return list(self.event_dispatcher.events)

    # --------------------------------------------------
    # EXECUTE  (generation flow)
    # --------------------------------------------------
    def execute(self, idea: str) -> FinalResponse:

        # Supervisor NEVER raises now — always returns valid dict
        self._setup_event_pipeline()
        assert self.event_dispatcher is not None
        self.event_dispatcher.reset()

        self._emit_agent_event("supervisor", "running")
        supervisor_result = self.supervisor.decide(idea)
        self._emit_agent_event("supervisor", "completed")

        selected = supervisor_result.get("selected_agents", [])
        reasoning = supervisor_result.get("reasoning", {})

        try:
            execution_plan = resolve_execution_plan(selected)
        except Exception as e:
            print(f"[Workflow] resolve_execution_plan failed: {e}")
            execution_plan = [
                "requirement",
                "architecture",
                "database",
                "api",
                "planner",
            ]

        requirement = None
        architecture = None
        database = None
        api = None
        plan = None
        errors = {}

        for agent_name in execution_plan:
            if agent_name == "requirement":
                self._emit_agent_event("requirement", "running")
                try:
                    requirement = self.requirement_agent.generate(idea)
                    self._emit_agent_event("requirement", "completed")
                except Exception as e:
                    print(f"[Workflow] RequirementAgent failed: {e}")
                    errors["requirement"] = str(e)
                    self._emit_agent_event(
                        "requirement",
                        "failed",
                        str(e),
                    )
                    requirement = RequirementResponse(
                        project_name=idea or "Untitled Project"
                    )

            elif agent_name == "architecture":
                self._emit_agent_event("architecture", "running")
                try:
                    architecture = self.architecture_agent.generate(requirement)
                    self._emit_agent_event("architecture", "completed")
                except Exception as e:
                    print(f"[Workflow] ArchitectureAgent failed: {e}")
                    errors["architecture"] = str(e)
                    self._emit_agent_event(
                        "architecture",
                        "failed",
                        str(e),
                    )

            elif agent_name == "database":
                self._emit_agent_event("database", "running")
                try:
                    database = self.database_agent.generate(requirement)
                    self._emit_agent_event("database", "completed")
                except Exception as e:
                    print(f"[Workflow] DatabaseAgent failed: {e}")
                    errors["database"] = str(e)
                    self._emit_agent_event(
                        "database",
                        "failed",
                        str(e),
                    )

            elif agent_name == "api":
                self._emit_agent_event("api", "running")
                try:
                    db_input = database if database is not None else _EMPTY_DB
                    api = self.api_agent.generate(requirement, db_input)
                    self._emit_agent_event("api", "completed")
                except Exception as e:
                    print(f"[Workflow] ApiAgent failed: {e}")
                    errors["api"] = str(e)
                    self._emit_agent_event(
                        "api",
                        "failed",
                        str(e),
                    )

            elif agent_name == "planner":
                self._emit_agent_event("planner", "running")
                try:
                    db_input = database if database is not None else _EMPTY_DB
                    api_input = api if api is not None else {}
                    plan = self.planner_agent.generate(requirement, db_input, api_input)
                    self._emit_agent_event("planner", "completed")
                except Exception as e:
                    print(f"[Workflow] PlannerAgent failed: {e}")
                    errors["planner"] = str(e)
                    self._emit_agent_event(
                        "planner",
                        "failed",
                        str(e),
                    )

        if errors:
            print(f"[Workflow] Completed with partial errors: {list(errors.keys())}")

        return FinalResponse(
            idea=idea,
            selected_agents=selected,
            execution_plan=execution_plan,
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

        self._setup_event_pipeline()
        assert self.event_dispatcher is not None
        self.event_dispatcher.reset()
        updated = deepcopy(blueprint)

        # Requirement always regenerates on update
        self._emit_agent_event("requirement", "running")
        try:
            requirement = self.requirement_agent.update(context)
            updated.requirements = requirement
            self._emit_agent_event("requirement", "completed")
        except Exception as e:
            print(f"[Workflow] RequirementAgent.update failed: {e}")
            requirement = blueprint.requirements  # keep existing
            updated.requirements = requirement
            self._emit_agent_event(
                "requirement",
                "failed",
                str(e),
            )

        # Preserve existing values as defaults
        architecture = blueprint.architecture
        database = blueprint.database
        api = blueprint.api
        plan = blueprint.plan

        try:
            execution_plan = resolve_execution_plan(selected)
        except Exception as e:
            print(f"[Workflow] resolve_execution_plan failed: {e}")
            execution_plan = [
                "requirement",
                "architecture",
                "database",
                "api",
                "planner",
            ]

        for agent_name in execution_plan:
            if agent_name == "requirement":
                # Requirement always regenerates on update
                continue

            if agent_name == "architecture":
                self._emit_agent_event("architecture", "running")
                try:
                    architecture = self.architecture_agent.generate(requirement)
                    updated.architecture = architecture
                    self._emit_agent_event("architecture", "completed")
                except Exception as e:
                    print(f"[Workflow] ArchitectureAgent update failed: {e}")
                    self._emit_agent_event(
                        "architecture",
                        "failed",
                        str(e),
                    )

            elif agent_name == "database":
                self._emit_agent_event("database", "running")
                try:
                    database = self.database_agent.generate(requirement)
                    updated.database = database
                    self._emit_agent_event("database", "completed")
                except Exception as e:
                    print(f"[Workflow] DatabaseAgent update failed: {e}")
                    self._emit_agent_event(
                        "database",
                        "failed",
                        str(e),
                    )

            elif agent_name == "api":
                self._emit_agent_event("api", "running")
                try:
                    db_input = database if database is not None else _EMPTY_DB
                    api = self.api_agent.generate(requirement, db_input)
                    updated.api = api
                    self._emit_agent_event("api", "completed")
                except Exception as e:
                    print(f"[Workflow] ApiAgent update failed: {e}")
                    self._emit_agent_event(
                        "api",
                        "failed",
                        str(e),
                    )

            elif agent_name == "planner":
                self._emit_agent_event("planner", "running")
                try:
                    db_input = database if database is not None else _EMPTY_DB
                    api_input = api if api is not None else {}
                    plan = self.planner_agent.generate(requirement, db_input, api_input)
                    updated.plan = plan
                    self._emit_agent_event("planner", "completed")
                except Exception as e:
                    print(f"[Workflow] PlannerAgent update failed: {e}")
                    self._emit_agent_event(
                        "planner",
                        "failed",
                        str(e),
                    )

        return FinalResponse(
            idea=blueprint.idea,
            selected_agents=selected,
            execution_plan=execution_plan,
            reasoning=reasoning,
            requirements=updated.requirements,
            architecture=updated.architecture,
            database=updated.database,
            api=updated.api,
            plan=updated.plan,
        )
