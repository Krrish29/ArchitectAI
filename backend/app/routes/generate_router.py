from fastapi import APIRouter
from app.schemas.generate_request import GenerateRequest
from app.schemas.final_response import FinalResponse
from app.agents.supervisor_agent import SupervisorAgent

router = APIRouter()


@router.post("/generate", response_model=FinalResponse)
def generate(req: GenerateRequest):

    supervisor = SupervisorAgent()

    return supervisor.execute(req.idea)
