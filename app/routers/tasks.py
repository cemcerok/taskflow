from fastapi import APIRouter, HTTPException, status
from app.schemas.task import TaskResponse, TaskCreate

router = APIRouter()


tasks = [
    {
        "id": 1,
        "title": "...",
        "completed": False
    },
    {
        "id": 2,
        "title": "...",
        "completed": True
    }
]

@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    return tasks

@router.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(task: TaskCreate):
    id_list = list(i["id"] for i in tasks)
    if len(id_list):
        max_id = max(id_list)
    else:
        max_id = 0

    task_dict = {"id": max_id + 1, **task.model_dump()}
    tasks.append(task_dict)

    return task_dict

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
