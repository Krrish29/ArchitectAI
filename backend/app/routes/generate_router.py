from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.orchestrator.workflow import Workflow

router = APIRouter()
workflow = Workflow()


class IdeaRequest(BaseModel):
    idea: str


@router.post("/generate")
def generate(req: IdeaRequest):
    try:
        return workflow.execute(req.idea)
    except Exception as e:
        print("GENERATION ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
