import time

from app.agents.requirement_agent import RequirementAgent
from app.agents.architecture_agent import ArchitectureAgent
from app.agents.planner_agent import PlannerAgent
from app.schemas.final_response import FinalResponse


class SupervisorAgent:

    def __init__(self):
        self.requirement_agent = RequirementAgent()
        self.architecture_agent = ArchitectureAgent()
        self.planner_agent = PlannerAgent()

    def execute(self, idea: str):

        workflow_start = time.time()

        print("\n" + "=" * 60)
        print("ARCHITECTAI :: MULTI-AGENT WORKFLOW")
        print("=" * 60)

        print("\nSTATUS : STARTED")
        print(f"PROJECT: {idea}")

        print("\nWORKFLOW:")
        print("USER_INPUT")
        print("     |")
        print("     v")
        print("SUPERVISOR_AGENT")
        print("     |")
        print("     +--> RequirementAgent")
        print("     |")
        print("     +--> ArchitectureAgent")
        print("     |")
        print("     +--> PlannerAgent")
        print("     |")
        print("     v")
        print("FINAL_BLUEPRINT")

        # STEP 1 : Requirement Agent
        print("\nSTEP 1 : RequirementAgent -> STARTED")

        start = time.time()
        requirements = self.requirement_agent.generate(idea)
        end = time.time()

        print(f"STEP 1 : RequirementAgent -> COMPLETED " f"({end - start:.2f}s)")

        # STEP 2 : Architecture Agent
        print("\nSTEP 2 : ArchitectureAgent -> STARTED")

        start = time.time()
        architecture = self.architecture_agent.generate(requirements)
        end = time.time()

        print(f"STEP 2 : ArchitectureAgent -> COMPLETED " f"({end - start:.2f}s)")

        # STEP 3 : Planner Agent
        print("\nSTEP 3 : PlannerAgent -> STARTED")

        start = time.time()
        plan = self.planner_agent.generate(requirements, architecture)
        end = time.time()

        print(f"STEP 3 : PlannerAgent -> COMPLETED " f"({end - start:.2f}s)")

        workflow_end = time.time()

        print(
            f"\nSTATUS : BLUEPRINT GENERATED " f"({workflow_end - workflow_start:.2f}s)"
        )
        print("=" * 60)

        return FinalResponse(
            idea=idea,
            requirements=requirements,
            architecture=architecture,
            plan=plan,
        )
