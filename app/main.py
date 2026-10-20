from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import inspect
from sqlalchemy.engine import Connection

from app.db.base import Base
from app.db.database import engine
from app.models.task import Task  # noqa: F401 - registers the table in metadata
from app.routers.health import router as health_router
from app.routers.tasks import router as tasks_router


def validate_database_schema(connection: Connection) -> None:
    """Fail clearly when create_all finds an incompatible existing table."""
    inspector = inspect(connection)
    task_columns = {column["name"] for column in inspector.get_columns("tasks")}
    required_columns = {"id", "title", "description", "completed", "created_at"}
    missing_columns = required_columns - task_columns

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise RuntimeError(
            "The existing 'tasks' table is incompatible with this application. "
            f"Missing columns: {missing}. Apply a database migration before startup; "
            "the application will not delete or modify existing data automatically."
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.run_sync(validate_database_schema)

    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(tasks_router)


@app.get("/")
async def read_root():
    return {"message": "TaskFlow API"}
