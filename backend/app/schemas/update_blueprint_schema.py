from typing import List

from pydantic import BaseModel, Field

from app.schemas.final_response import FinalResponse


class UpdateBlueprintRequest(BaseModel):
    """
    Request received by POST /update-blueprint.
    """

    project_id: str = Field(..., description="Unique project identifier.")

    instruction: str = Field(
        ...,
        min_length=1,
        description="Natural language instruction describing the requested blueprint modification.",
    )

    blueprint: FinalResponse = Field(
        ..., description="Current blueprint that should be updated."
    )


class UpdateBlueprintResponse(BaseModel):
    """
    Response returned after updating the blueprint.
    """

    blueprint: FinalResponse = Field(..., description="Updated blueprint.")

    executed_agents: List[str] = Field(
        default_factory=list, description="Agents executed while processing the update."
    )
