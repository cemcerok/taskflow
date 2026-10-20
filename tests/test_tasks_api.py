import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.database import get_db
from app.routers.tasks import router as tasks_router


@pytest_asyncio.fixture
async def client():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
    )
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with session_factory() as session:
            yield session

    test_app = FastAPI()
    test_app.include_router(tasks_router)
    test_app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url="http://test",
    ) as test_client:
        yield test_client

    await engine.dispose()


@pytest.mark.asyncio
async def test_task_crud(client: AsyncClient):
    response = await client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

    response = await client.post(
        "/tasks",
        json={"title": "First task", "description": "Initial description"},
    )
    assert response.status_code == 201
    created = response.json()
    task_id = created["id"]
    assert created["completed"] is False
    assert created["created_at"] is not None

    response = await client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "First task"

    response = await client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Replaced task",
            "description": "Replacement description",
            "completed": False,
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Replaced task"

    response = await client.patch(
        f"/tasks/{task_id}",
        json={"description": None, "completed": True},
    )
    assert response.status_code == 200
    patched = response.json()
    assert patched["title"] == "Replaced task"
    assert patched["description"] is None
    assert patched["completed"] is True

    response = await client.patch(f"/tasks/{task_id}", json={"title": None})
    assert response.status_code == 422

    response = await client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    assert response.content == b""

    response = await client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

    response = await client.get("/tasks/999999")
    assert response.status_code == 404
