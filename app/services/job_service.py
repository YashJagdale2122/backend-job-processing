from app.infrastructure.db.repositories.job_repository import JobRepository
from app.infrastructure.db.models.job_model import JobModel
from app.domain.enums import JobStatus

class JobService:
    def __init__(self, repo: JobRepository):
        self.repo = repo

    def create_job(self, payload: dict) -> JobModel:
        job = JobModel(
            payload=payload,
            status=JobStatus.PENDING,
        )
        return self.repo.create(job)

    def mark_running(self, job: JobModel):
        job.status = JobStatus.RUNNING
        return self.repo.save(job)

    def mark_success(self, job: JobModel, result: dict):
        job.status = JobStatus.COMPLETED
        job.result = result
        return self.repo.save(job)

    def mark_failed(self, job: JobModel, error: str):
        job.retries += 1
        job.last_error = error

        if job.retries >= job.max_retries:
            job.status = JobStatus.FAILED
        else:
            job.status = JobStatus.RETRYING

        return self.repo.save(job)
