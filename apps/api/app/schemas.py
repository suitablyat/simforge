from pydantic import BaseModel
from typing import Literal, Optional
from uuid import UUID

JobStatus = Literal["queued", "running", "succeeded", "failed"]

class JobCreate(BaseModel):
    note: Optional[str] = None

class Job(BaseModel):
    id: UUID
    status: JobStatus
    note: Optional[str] = None
