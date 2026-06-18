from app.agents.requirement_agent import RequirementAgent
from app.agents.architecture_agent import ArchitectureAgent
from app.agents.planner_agent import PlannerAgent


class Workflow:

    def execute(self, idea: str):

        requirement_agent = RequirementAgent()
        architecture_agent = ArchitectureAgent()
        planner_agent = PlannerAgent()

        requirements = requirement_agent.generate(idea)

        architecture = architecture_agent.generate(requirements)

        project_plan = planner_agent.generate(requirements)

        return {
    "requirements": requirements.model_dump(),
    "architecture": architecture,
    "project_plan": project_plan
        }