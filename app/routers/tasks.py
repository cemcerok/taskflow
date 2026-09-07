from fastapi import APIRouter, HTTPException, status

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

@router.get("/tasks")
def get_tasks():
    return tasks

@router.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
