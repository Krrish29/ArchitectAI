from pydantic import BaseModel
from typing import Any, Optional


class StreamEvent(BaseModel):
    type: str
    agent: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None
    data: Optional[Any] = None
