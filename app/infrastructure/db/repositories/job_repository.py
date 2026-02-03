from sqlalchemy.orm import Session

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

    def get_by_id(self, job_id: UUID):
        return self.db.query(JobModel).filter(JobModel.id == job_id).first()

    def save(self, job: JobModel) -> JobModel:
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_next_pending(self) -> JobModel | None:
        return (
            self.db.query(JobModel)
            .filter(JobModel.status == JobStatus.PENDING)
            .order_by(JobModel.created_at)
            .first()
        )
