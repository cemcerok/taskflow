from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.tasks import router as tasks_router

app = FastAPI()


app.include_router(health_router)
app.include_router(tasks_router)

@app.get("/")
def read_root():
    return {"message": "TaskFlow API"}
