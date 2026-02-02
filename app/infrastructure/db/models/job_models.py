from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base
from app.domain.enums import JobStatus, JobType


class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    type = Column(Enum(JobType), nullable=False)
    status = Column(Enum(JobStatus), nullable=False)

    attempt = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    error = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
