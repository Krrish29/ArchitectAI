from typing import Callable, Optional

from app.schemas.stream_event import StreamEvent


class EventDispatcher:
    def __init__(
        self,
        callback: Optional[Callable[[StreamEvent], None]] = None,
    ):
        self.callback = callback

    def dispatch(
        self,
        event: StreamEvent,
    ):
        if self.callback:
            self.callback(event)
