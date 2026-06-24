from fastapi import APIRouter
from app.schemas.generate_request import GenerateRequest
from app.schemas.final_response import FinalResponse
from app.orchestrator.workflow import Workflow

router = APIRouter()

workflow = Workflow()


@router.post("/generate", response_model=FinalResponse)
def generate(req: GenerateRequest):
    return workflow.execute(req.idea)
