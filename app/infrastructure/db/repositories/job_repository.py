from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.infrastructure.db.models.job_models import JobModel
from app.domain.enums import JobStatus


class JobRepository:
    """
    Repository responsible for all Job DB operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_job(self, job: JobModel) -> JobModel:
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_by_id(self, job_id: UUID) -> Optional[JobModel]:
        return (
            self.db.query(JobModel)
            .filter(JobModel.id == job_id)
            .first()
        )

    def save(self, job: JobModel) -> JobModel:
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_next_pending(self) -> Optional[JobModel]:
        return (
            self.db.query(JobModel)
            .filter(JobModel.status == JobStatus.PENDING)
            .order_by(JobModel.created_at)
            .first()
        )
