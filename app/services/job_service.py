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

    def mark_failed(self, job: JobModel, error: str) -> JobModel:
        job.last_error = error
        job.retries += 1

        if job.retries >= job.max_retries:
            return self.job_repo.update_status(job, JobStatus.FAILED)

        return self.job_repo.update_status(job, JobStatus.RETRYING)

    def requeue(self, job: JobModel) -> JobModel:
        """
        Move a RETRYING job back to PENDING.
        """
        if job.status != JobStatus.RETRYING:
            return job

        return self.job_repo.update_status(job, JobStatus.PENDING)

    def execute_job(self, job: JobModel) -> JobModel:
        if job.status in (JobStatus.RUNNING, JobStatus.COMPLETED):
            return job
