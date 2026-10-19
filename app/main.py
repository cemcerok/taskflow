from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.routers.health import router as health_router
from app.routers.tasks import router as tasks_router
from app.db.base import Base
from app.db.database import engine
from app.models.task import Task 

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(tasks_router)

@app.get("/")
def read_root():
    return {"message": "TaskFlow API"}
