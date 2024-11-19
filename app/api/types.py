from pydantic import BaseModel, Field # type: ignore
from typing import Optional # type: ignore

class JobCreateRequest(BaseModel):
    type: str
    input: str

class JobResponse(BaseModel):
    id: int
    type: str
    status: str
    started_at: float
    ended_at: float
    input: str
    output: str
