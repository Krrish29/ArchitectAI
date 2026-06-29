from typing import List

from pydantic import BaseModel

from app.schemas.final_response import FinalResponse
from app.schemas.stream_event import StreamEvent


class ExecutionResponse(BaseModel):
    result: FinalResponse
    events: List[StreamEvent] = []
