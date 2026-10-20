from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskChange, TaskCreate, TaskPatch


async def get_tasks(session: AsyncSession) -> list[Task]:
    result = await session.execute(select(Task).order_by(Task.id))
    return list(result.scalars().all())


async def get_task_by_id(session: AsyncSession, task_id: int) -> Task | None:
    result = await session.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def create_task(session: AsyncSession, task_create: TaskCreate) -> Task:
    task = Task(**task_create.model_dump())
    session.add(task)

    try:
        await session.commit()
        await session.refresh(task)
    except SQLAlchemyError:
        await session.rollback()
        raise

    return task


async def update_task(
    session: AsyncSession,
    task: Task,
    task_change: TaskChange,
) -> Task:
    for field, value in task_change.model_dump().items():
        setattr(task, field, value)

    try:
        await session.commit()
        await session.refresh(task)
    except SQLAlchemyError:
        await session.rollback()
        raise

    return task


async def patch_task(
    session: AsyncSession,
    task: Task,
    task_patch: TaskPatch,
) -> Task:
    for field, value in task_patch.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    try:
        await session.commit()
        await session.refresh(task)
    except SQLAlchemyError:
        await session.rollback()
        raise

    return task


async def delete_task(session: AsyncSession, task: Task) -> None:
    try:
        await session.delete(task)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
