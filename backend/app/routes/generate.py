from fastapi import APIRouter
from app.schemas.request_schema import IdeaRequest
from app.schemas.final_response import FinalResponse
from app.agents.supervisor_agent import SupervisorAgent

router = APIRouter()

supervisor = SupervisorAgent()


@router.post("/generate", response_model=FinalResponse)
def generate(data: IdeaRequest):
    return supervisor.execute(data.idea)
