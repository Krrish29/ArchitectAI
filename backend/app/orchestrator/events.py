from enum import Enum


class EventType(str, Enum):
    AGENT = "agent"
    RESULT = "result"
    ERROR = "error"


class AgentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
