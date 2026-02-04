from app.infrastructure.db.repositories.job_repository import JobRepository
from app.infrastructure.db.models.job_models import JobModel
from app.domain.enums import JobStatus


class JobService:
    def __init__(self, repo: JobRepository):
        self.repo = repo

    def create_job(self, payload: dict) -> JobModel:
        job = JobModel(
            payload=payload,
            status=JobStatus.PENDING,
            retries=0,
        )
        return self.repo.create_job(job)

    def get_job(self, job_id):
        return self.repo.get_by_id(job_id)

    def mark_running(self, job: JobModel) -> JobModel:
        job.status = JobStatus.RUNNING
        return self.repo.save(job)

    def mark_success(self, job: JobModel, result: dict) -> JobModel:
        job.status = JobStatus.COMPLETED
        job.result = result
        return self.repo.save(job)

    def mark_failed(self, job: JobModel, error: str) -> JobModel:
        job.last_error = error
        job.retries += 1

        if job.retries >= job.max_retries:
            job.status = JobStatus.FAILED
        else:
            job.status = JobStatus.RETRYING

        return self.repo.save(job)

    def requeue(self, job: JobModel) -> JobModel:
        if job.status != JobStatus.RETRYING:
            return job

        job.status = JobStatus.PENDING
        return self.repo.save(job)

    def execute_job(self, job: JobModel) -> JobModel:
        """
        Core execution entrypoint.
        """
        if job.status != JobStatus.PENDING:
            return job

        self.mark_running(job)

        try:

            result = {"message": "job executed successfully"}
            return self.mark_success(job, result)

        except Exception as exc:
            return self.mark_failed(job, str(exc))
