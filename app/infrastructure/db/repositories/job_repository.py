from sqlalchemy.orm import Session
from typing import Optional, List

from app,infrastructure.db.models.job_models import JobModel
from app.domain.enums import JobStatus

class JobRepository:
    """
    Repository responsible for all Job DB operations.
    """
    def.__init__(self, db: Session):
        self.db = db

    def create_job(self, job: JobModel) -> JobModel:
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_by_id(self, job_id: int) -> Optional[JobModel]:
        return(
            self.db.query(JobModel)
            .filter(JobModel.id == job_id)
            .first()
        )

    def get_by_status(self, status: JobStatus) -> List[JobModel]:
        return(
            self.db.query(JobModel)
            .filter(JobModel.status == status)
            .all()
        )

    def update_status(self, job: JobModel, status: JobStatus) -> JobModel:
        job.status = status
        self.db.commit()
        self.db.refresh(job)
        return job
