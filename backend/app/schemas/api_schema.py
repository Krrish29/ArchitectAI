from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional, Any


class Endpoint(BaseModel):
    model_config = ConfigDict(extra="ignore")

    method: str = "GET"
    path: str = "/"
    description: str = ""
    request_body: Optional[Any] = None
    response: Optional[Any] = None

    @field_validator("method", mode="before")
    @classmethod
    def normalise_method(cls, v):
        if not v or not isinstance(v, str):
            return "GET"
        return v.upper()

    @field_validator("path", mode="before")
    @classmethod
    def normalise_path(cls, v):
        if not v or not isinstance(v, str):
            return "/"
        return v


class ApiResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    base_url: str = "/api"
    endpoints: List[Endpoint] = []
    request_schemas: List[Any] = []
    response_schemas: List[Any] = []

    @field_validator("base_url", mode="before")
    @classmethod
    def normalise_base_url(cls, v):
        if not v or not isinstance(v, str):
            return "/api"
        return v

    @field_validator("endpoints", mode="before")
    @classmethod
    def normalise_endpoints(cls, v):
        if not isinstance(v, list):
            return []
        return [item for item in v if isinstance(item, dict)]

    @field_validator("request_schemas", "response_schemas", mode="before")
    @classmethod
    def normalise_schema_lists(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        return [v]
