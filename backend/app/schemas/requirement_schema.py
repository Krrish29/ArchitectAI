from pydantic import BaseModel
from typing import List


class RequirementResponse(BaseModel):
    project_name: str
    features: List[str]
    functional_requirements: List[str]
    non_functional_requirements: List[str]