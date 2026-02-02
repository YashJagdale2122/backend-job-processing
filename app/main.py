from fastapi import FastAPI

from app.infrastructure.db.init_db import init_db
from app.api.routes import jobs
app = FastAPI(title="Backend Job Processing System")



app.include_router(jobs.router)

@app.on_event("startup")
def startup_event():
    init_db()
