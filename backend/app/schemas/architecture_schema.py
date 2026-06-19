from pydantic import BaseModel
from typing import List


class ArchitectureResponse(BaseModel):
    architecture_type: str
    frontend: List[str]
    backend: List[str]
    database: List[str]
    authentication: List[str]
    services: List[str]
    deployment: List[str]