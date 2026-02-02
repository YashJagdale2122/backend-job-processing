from typing import Optional

from app.infrastructure.db.repositories.job_repository import JobRepository
from app.infrastructure.db.models.job_model import JobModel
from app.domain.enums import JobStatus

class JobService:
    """
    Business logic for job lifecycle.
    """

    def __init__(self, job_repo: JobRepository):
        self.job_repo = job_repo

    def create_job(self, payload: dict) -> JobModel:
        """
        Create a new job in PENDING state.
        """
        job=JobModel(
            payload=payload,
            status=JobStatus.PENDING,
            retries=0;
        )
        return self.job_repo.create_job(job)

    def get_job(self, job_id: int) -> Optional[JobModel]:
        return self.job_repo.get_by_id(job_id)

    def mark_running(self, job: JobModel) -> JobModel:
        return self.job_repo.update_status(job, JobStatus.RUNNING)

    def mark_success(self, job: JobModel, result: dict) -> JobModel:
        job.result = result
        return self.job_repo.update_status(job, JobStatus.SUCCESS)

    def mark_failed(self, job: JobModel, error: str) -> JobModel:
        job.last_error = error
        job.retries += 1

        if job.retries >= job.max_retries:
            return self.job_repo.update_status(job, JobStatus.FAILED)

        return self.job_repo.update_status(job, JobStatus.PENDING)
