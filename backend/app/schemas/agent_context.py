from typing import Optional

from pydantic import BaseModel


class AgentContext(BaseModel):
    """
    Shared context passed between all agents.

    During initial blueprint generation:
    - idea is populated
    - instruction is None

    During blueprint updates:
    - instruction contains the user's modification request
    - existing blueprint sections are already populated
    """

    idea: Optional[str] = None
    instruction: Optional[str] = None

    requirements: Optional[str] = None
    architecture: Optional[str] = None
    database: Optional[str] = None
    api: Optional[str] = None
    plan: Optional[str] = None
