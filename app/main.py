from fastapi import FastAPI
from app.infrastructure.db.init_db import init_db

app = FastAPI(title="Backend Job Processing System")


@app.on_event("startup")
def startup_event():
    init_db()
