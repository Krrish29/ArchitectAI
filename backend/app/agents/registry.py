from app.agents.requirement_agent import RequirementAgent
from app.agents.architecture_agent import ArchitectureAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.database_agent import DatabaseAgent
from app.agents.api_agent import ApiAgent

AGENTS = {
    "requirement": RequirementAgent(),
    "architecture": ArchitectureAgent(),
    "database": DatabaseAgent(),
    "api": ApiAgent(),
    "planner": PlannerAgent(),
}
