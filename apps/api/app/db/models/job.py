from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid, enum
from app.db.base import Base

class JobStatus(str, enum.Enum):
    queued="queued"; running="running"; done="done"; failed="failed"

class Job(Base):
    __tablename__ = "jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    note = Column(String, nullable=True)
    status = Column(Enum(JobStatus, name="job_status"), nullable=False, default=JobStatus.queued)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
