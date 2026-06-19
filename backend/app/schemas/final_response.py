from pydantic import BaseModel
from app.schemas.requirement_schema import RequirementResponse
from app.schemas.architecture_schema import ArchitectureResponse
from app.schemas.planner_schema import PlannerResponse


class FinalResponse(BaseModel):
    idea: str
    requirements: RequirementResponse
    architecture: ArchitectureResponse
    plan: PlannerResponse
