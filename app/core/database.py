from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclaretiveBase

from app.core.config import settings

class Base(DeclaretiveBase):
    pass

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
