from pydantic import BaseModel, Field
from typing import Any

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)

class AskResponse(BaseModel):
    question: str
    generated_sql: str
    results: list[dict[str, Any]]
    row_count: int