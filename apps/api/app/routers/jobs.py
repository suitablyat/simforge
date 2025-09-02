from fastapi import APIRouter, HTTPException
from uuid import uuid4, UUID
from app.routers import memory_store
from app.schemas import Job, JobCreate


router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("", response_model=Job, status_code=201)
def create_job(payload: JobCreate):
    job_id = uuid4()
    job = Job(id=job_id, status="queued", note=payload.note)
    memory_store.JOBS[str(job_id)] = job.model_dump()
    return job

@router.get("/{job_id}", response_model=Job)
def get_job(job_id: UUID):
    data = memory_store.JOBS.get(str(job_id))
    if not data:
        raise HTTPException(status_code=404, detail="Job not found")
    return Job(**data)
