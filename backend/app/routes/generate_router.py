import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.orchestrator.workflow import Workflow

logger = logging.getLogger(__name__)

router = APIRouter()
workflow = Workflow()


class IdeaRequest(BaseModel):
    idea: str


@router.post("/generate")
def generate(req: IdeaRequest):
    try:
        return workflow.execute(req.idea)
    except Exception:
        logger.exception("Blueprint generation failed")
        raise HTTPException(
            status_code=500, detail="Failed to generate blueprint. Please try again."
        )
