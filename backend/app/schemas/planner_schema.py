from pydantic import BaseModel
from typing import List


class Phase(BaseModel):
    phase_name: str
    tasks: List[str]


class PlannerResponse(BaseModel):
    phases: List[Phase]
