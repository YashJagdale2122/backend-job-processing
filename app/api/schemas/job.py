from pydantic import BaseModel
from typing import Optional, Dict
from app.domain.enums import JobStatus
from uuid import UUID

class JobCreateRequest(BaseModel):
    payload: Dict


class JobResponse(BaseModel):
    id: UUID
    status: JobStatus
    retries: int
    result: Optional[Dict] = None
    last_error: Optional[str] = None

    class Config:
        from_attributes = True
