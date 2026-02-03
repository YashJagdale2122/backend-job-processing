from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import Generator

class Base(DeclarativeBase):
    pass

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
