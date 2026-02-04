import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.infrastructure.db.models.job_models import JobModel
from app.infrastructure.db.repositories.job_repository import JobRepository
from app.services.job_service import JobService
from app.domain.enums import JobStatus


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def job_service(db_session):
    repo = JobRepository(db_session)
    return JobService(repo)


def test_create_job(job_service):
    job = job_service.create_job(payload={"task": "test"})

    assert job.status == JobStatus.PENDING
    assert job.retries == 0
    assert job.payload["task"] == "test"


def test_successful_job_execution(job_service):
    job = job_service.create_job(payload={"task": "success"})

    job_service.execute_job(job)

    assert job.status == JobStatus.COMPLETED
    assert job.result is not None


def test_retry_then_fail(job_service):
    job = job_service.create_job(payload={"task": "fail"})
    job.max_retries = 2

    # First attempt → retry
    job_service.mark_running(job)
    job_service.mark_failed(job, "error")
    job_service.requeue(job)

    assert job.status == JobStatus.PENDING
    assert job.retries == 1

    # Second attempt → terminal failure
    job_service.mark_running(job)
    job_service.mark_failed(job, "error again")

    assert job.status == JobStatus.FAILED
    assert job.retries == 2
