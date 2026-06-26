from pydantic import BaseModel

from app.schemas.final_response import FinalResponse


class BlueprintUpdateContext(BaseModel):
    """
    Shared context passed to update-capable agents.

    It contains the user's modification request together with the
    current blueprint so agents can regenerate only their own section.
    """

    instruction: str
    blueprint: FinalResponse
