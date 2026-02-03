from sqlalchemy import Column, DateTime, Enum, Integer, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    type = Column(Enum(JobType), nullable=False, default=JobType.GENERIC)
    status = Column(Enum(JobStatus), nullable=False)

    payload = Column(JSON, nullable=False)
    result = Column(JSON, nullable=True)

    retries = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    last_error = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
