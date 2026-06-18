from fastapi import APIRouter
from app.schemas.request_schema import IdeaRequest
from app.orchestrator.workflow import Workflow

router = APIRouter(
    prefix="/api",
    tags=["ArchitectAI"]
)


@router.post("/generate")
def generate(request: IdeaRequest):
    workflow = Workflow()
    result = workflow.execute(request.idea)
    return result