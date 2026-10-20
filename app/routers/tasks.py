from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repositories import task as task_repository
from app.schemas.task import TaskChange, TaskCreate, TaskPatch, TaskResponse

router = APIRouter()
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(session: DatabaseSession):
    return await task_repository.get_tasks(session)


@router.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task(task: TaskCreate, session: DatabaseSession):
    return await task_repository.create_task(session, task)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_by_id(task_id: int, session: DatabaseSession):
    task = await task_repository.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def change_task(
    task_id: int,
    task_change: TaskChange,
    session: DatabaseSession,
):
    task = await task_repository.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return await task_repository.update_task(session, task, task_change)


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def patch_task(
    task_id: int,
    task_patch: TaskPatch,
    session: DatabaseSession,
):
    task = await task_repository.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return await task_repository.patch_task(session, task, task_patch)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: DatabaseSession) -> Response:
    task = await task_repository.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    await task_repository.delete_task(session, task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
