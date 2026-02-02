from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.job import JobCreateRequest, JobResponse
from app.core.database import get_db
from app.infrastructure.db.repositories.job_repository import JobRepository
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["Jobs"])


def get_job_service(db: Session = Depends(get_db)) -> JobService:
    repo = JobRepository(db)
    return JobService(repo)


@router.post("/", response_model=JobResponse)
def create_job(
    request: JobCreateRequest,
    service: JobService = Depends(get_job_service),
):
    job = service.create_job(request.payload)
    return job


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    service: JobService = Depends(get_job_service),
):
    job = service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
