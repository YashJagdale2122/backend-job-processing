from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.enums import JobStatus, JobType

@dataclass
class Job:
    """
    Domain model representing a background Job.
    """
    id : UUID = field(default_factory=uuid4)
    tyoe : JobType = JobType.GENERIC
    status : JobStatus  = JobStatus.PENDING

    attempt : int = 0
    max_retries : int = 3

    error : str | None = None

    created_at : datetime = field(default_factory=datetime.utcnow)
    updated_at : datetime = field(default_factory=datetime.utcnow)

    def can_retry(self) -> bool:
        return self.attempt < self.max_retries

    def mark_running(self) -> None:
        self.status = JobStatus.RUNNING
        self.updated_at = datetime.utcnow()

    def mark_completed(self) -> None:
        self.status = JobStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def mark_failed(self, error : str) -> None:
        self.error = error
        self.attempt +=1
        self.updated_at = datetime.utcnow()

        if self.can_retry():
            self.JobStatus = JobStatus.RETRYING
        else:
            self.JobStatus = JobStatus.FAILED
