from typing import Optional, List, Dict
from pydantic import BaseModel

from app.schemas.requirement_schema import RequirementResponse
from app.schemas.architecture_schema import ArchitectureResponse
from app.schemas.database_schema import DatabaseResponse
from app.schemas.api_schema import ApiResponse
from app.schemas.planner_schema import PlannerResponse


class FinalResponse(BaseModel):
    idea: str

    selected_agents: List[str] = []

    execution_plan: List[str] = []

    reasoning: Dict[str, str] = {}

    requirements: Optional[RequirementResponse] = None

    architecture: Optional[ArchitectureResponse] = None

    database: Optional[DatabaseResponse] = None

    api: Optional[ApiResponse] = None

    plan: Optional[PlannerResponse] = None
