from typing import List, Dict
from pydantic import BaseModel


class SupervisorResponse(BaseModel):
    selected_agents: List[str]
    reasoning: Dict[str, str] = {}
