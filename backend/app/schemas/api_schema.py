from pydantic import BaseModel
from typing import List


class ApiResponse(BaseModel):
    endpoints: List[str]
    request_schemas: List[str]
    response_schemas: List[str]
