from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional, Any


class Phase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phase_name: str = "Unnamed Phase"
    tasks: List[str] = []
    dependencies: List[Any] = []
    estimated_duration_days: Optional[int] = None

    @field_validator("tasks", mode="before")
    @classmethod
    def normalise_tasks(cls, v):
        if isinstance(v, list):
            return [str(t) for t in v]
        if isinstance(v, str):
            return [v]
        return []

    @field_validator("tasks", mode="after")
    @classmethod
    def ensure_nonempty_tasks(cls, v):
        return v if v else ["Implementation details TBD"]

    @field_validator("dependencies", mode="before")
    @classmethod
    def normalise_deps(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        return []


class Milestone(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = ""
    description: str = ""


class PlannerResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phases: List[Phase] = []
    timeline: str = "4-6 weeks"
    milestones: List[Milestone] = []

    @field_validator("phases", mode="before")
    @classmethod
    def normalise_phases(cls, v):
        if not isinstance(v, list):
            return []
        result = []
        for item in v:
            if isinstance(item, dict):
                result.append(item)  # pass through to Phase validator
            elif isinstance(item, str):
                # SafeLLM.ensure_string_list stringified dicts — try to recover
                try:
                    import ast

                    parsed = ast.literal_eval(item)
                    if isinstance(parsed, dict):
                        result.append(parsed)
                    else:
                        result.append({"phase_name": item, "tasks": []})
                except Exception:
                    result.append({"phase_name": item, "tasks": []})
        return result

    @field_validator("milestones", mode="before")
    @classmethod
    def normalise_milestones(cls, v):
        if not isinstance(v, list):
            return []
        result = []
        for item in v:
            if isinstance(item, dict):
                result.append(item)
            elif isinstance(item, str):
                try:
                    import ast

                    parsed = ast.literal_eval(item)
                    if isinstance(parsed, dict):
                        result.append(parsed)
                    else:
                        result.append({"name": item, "description": ""})
                except Exception:
                    result.append({"name": item, "description": ""})
        return result
