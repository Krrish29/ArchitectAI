from typing import Callable, Optional

from app.orchestrator.events import EventType
from app.schemas.stream_event import StreamEvent


class WorkflowEventEmitter:
    def __init__(self, callback: Optional[Callable] = None):
        self.callback = callback

    def emit(
        self,
        agent: str,
        status: str,
        message: str = "",
    ):
        event = StreamEvent(
            type=EventType.AGENT.value,
            agent=agent,
            status=status,
            message=message,
        )
        if self.callback:
            self.callback(event)
