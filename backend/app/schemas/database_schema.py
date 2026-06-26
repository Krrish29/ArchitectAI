from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Union


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
                result.append(item.get("name") or item.get("description") or str(item))
            else:
                result.append(str(item))
        return result
    return [str(v)]


class Entity(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str = "Entity"
    type: str = ""
    description: str = ""

    @field_validator("name", mode="before")
    @classmethod
    def normalise_name(cls, v):
        if not v or not isinstance(v, str):
            return "Entity"
        return v


class DatabaseResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    database: str = "PostgreSQL"
    entities: List[Entity] = []
    relationships: List[str] = []
    indexes: List[str] = []

    @field_validator("database", mode="before")
    @classmethod
    def normalise_database(cls, v):
        if not v or not isinstance(v, str):
            return "PostgreSQL"
        return v

    @field_validator("entities", mode="before")
    @classmethod
    def normalise_entities(cls, v):
        if not isinstance(v, list):
            return []
        result = []
        for item in v:
            if isinstance(item, dict):
                result.append(item)
            elif isinstance(item, str):
                result.append({"name": item, "type": "", "description": ""})
        return result

    @field_validator("relationships", "indexes", mode="before")
    @classmethod
    def normalise_string_lists(cls, v):
        return _coerce_string_list(v)
