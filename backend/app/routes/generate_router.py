import json
import logging
from queue import Queue
from threading import Thread

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from app.orchestrator.workflow import Workflow
from app.schemas.execution_response import ExecutionResponse

logger = logging.getLogger(__name__)
router = APIRouter()


class IdeaRequest(BaseModel):
    idea: str


def _format_sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def _generate_event_stream(idea: str):
    queue: Queue = Queue()

    def send_event(event_name: str, payload: dict):
        queue.put(_format_sse(event_name, payload))

    def run_workflow():
        try:
            workflow = Workflow(
                event_callback=lambda event: send_event("agent", event.dict())
            )
            result = workflow.execute(idea)
            send_event(
                "result",
                {
                    "result": result.dict(),
                    "events": [event.dict() for event in workflow.get_events()],
                },
            )
        except Exception as exc:
            logger.exception("Blueprint streaming failed")
            send_event("error", {"message": str(exc)})
        finally:
            queue.put(None)

    thread = Thread(target=run_workflow, daemon=True)
    thread.start()

    while True:
        chunk = queue.get()
        if chunk is None:
            break
        yield chunk


@router.post("/generate", response_model=ExecutionResponse)
def generate(req: IdeaRequest):
    try:
        workflow = Workflow()
        result = workflow.execute(req.idea)
        return ExecutionResponse(result=result, events=workflow.get_events())
    except Exception:
        logger.exception("Blueprint generation failed")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate blueprint. Please try again.",
        )


@router.get("/generate-stream")
def generate_stream(idea: str):
    return StreamingResponse(
        _generate_event_stream(idea),
        media_type="text/event-stream",
    )
