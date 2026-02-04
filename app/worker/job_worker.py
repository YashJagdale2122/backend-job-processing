import time
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.infrastructure.db.repositories.job_repository import JobRepository
from app.services.job_service import JobService
from app.domain.enums import JobStatus


POLL_INTERVAL = 2  # seconds


def run_worker() -> None:
    print("🚀 Job worker started")

    while True:
        db: Session = SessionLocal()
        try:
            repo = JobRepository(db)
            service = JobService(repo)

            job = repo.get_next_pending()

            if not job:
                time.sleep(POLL_INTERVAL)
                continue

            try:
                service.execute_job(job)
            except Exception:
                # absolute safety net
                service.mark_failed(job, "Worker crashed")
            finally:
                if job.status == JobStatus.RETRYING:
                    service.requeue(job)


        finally:
            db.close()

if __name__ == "__main__":
    run_worker()
