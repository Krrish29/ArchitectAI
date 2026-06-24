from pydantic import BaseModel
from typing import List


class DatabaseResponse(BaseModel):
    database: str
    entities: List[str]
    relationships: List[str]
    indexes: List[str]
