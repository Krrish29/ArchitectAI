from pydantic import BaseModel, ConfigDict, field_validator
from typing import List


def _coerce_string_list(v):
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    if isinstance(v, list):
        result = []
        for item in v:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, dict):
                # Rule #5 says "no objects in arrays", but be defensive anyway
                result.append(
                    item.get("name")
                    or item.get("title")
                    or item.get("description")
                    or str(item)
                )
            else:
                result.append(str(item))
        return result
    return [str(v)]


class RequirementResponse(BaseModel):
    model_config = ConfigDict(
        extra="ignore"
    )  # tolerate extra LLM fields here; this isn't UI-breaking like Planner's was

    project_name: str = "Untitled Project"
    features: List[str] = []
    functional_requirements: List[str] = []
    non_functional_requirements: List[str] = []

    @field_validator(
        "features",
        "functional_requirements",
        "non_functional_requirements",
        mode="before",
    )
    @classmethod
    def normalise_lists(cls, v):
        return _coerce_string_list(v)

    @field_validator("project_name", mode="before")
    @classmethod
    def normalise_project_name(cls, v):
        if not v or not isinstance(v, str):
            return "Untitled Project"
        return v
