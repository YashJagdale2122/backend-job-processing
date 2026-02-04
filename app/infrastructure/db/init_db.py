from app.core.database import Base, engine

# Import ALL models here
from app.infrastructure.db.models.job_models import JobModel  # noqa: F401


def init_db() -> None:
    """
    Initialize database tables.
    Safe to call multiple times.
    """
    Base.metadata.create_all(bind=engine)
