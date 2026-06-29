from typing import Callable, Optional

from app.schemas.stream_event import StreamEvent


class EventDispatcher:
    def __init__(
        self,
        callback: Optional[Callable[[StreamEvent], None]] = None,
    ):
        self.callback = callback
        self.events: list[StreamEvent] = []

    def dispatch(
        self,
        event: StreamEvent,
    ):
        self.events.append(event)
        if self.callback:
            self.callback(event)

    def reset(self):
        self.events = []
