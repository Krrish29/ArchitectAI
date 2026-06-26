from typing import Callable, Optional


class WorkflowEventEmitter:
    def __init__(self, callback: Optional[Callable] = None):
        self.callback = callback

    def emit(
        self,
        agent: str,
        status: str,
        message: str = "",
    ):
        if self.callback:
            self.callback(
                {
                    "agent": agent,
                    "status": status,
                    "message": message,
                }
            )
