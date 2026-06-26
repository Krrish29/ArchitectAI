from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional


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
                result.append(
                    item.get("name")
                    or item.get("tech")
                    or item.get("title")
                    or str(item)
                )
            else:
                result.append(str(item))
        return result
    return [str(v)]


class AdditionalFeature(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str = "Feature"
    details: str = ""

    @field_validator("name", mode="before")
    @classmethod
    def normalise_name(cls, v):
        if not v or not isinstance(v, str):
            return "Feature"
        return v


class ArchitectureResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    architecture_type: str = "Microservices"
    frontend: List[str] = []
    backend: List[str] = []
    database: List[str] = []
    authentication: List[str] = []
    services: List[str] = []
    deployment: List[str] = []
    additional_features: List[AdditionalFeature] = []

    @field_validator(
        "frontend",
        "backend",
        "database",
        "authentication",
        "services",
        "deployment",
        mode="before",
    )
    @classmethod
    def normalise_lists(cls, v):
        return _coerce_string_list(v)

    @field_validator("architecture_type", mode="before")
    @classmethod
    def normalise_type(cls, v):
        if not v or not isinstance(v, str):
            return "Microservices"
        return v

    @field_validator("additional_features", mode="before")
    @classmethod
    def normalise_additional_features(cls, v):
        if not isinstance(v, list):
            return []
        result = []
        for item in v:
            if isinstance(item, dict):
                result.append(item)
            elif isinstance(item, str):
                result.append({"name": item, "details": ""})
        return result
