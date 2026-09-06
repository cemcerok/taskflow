from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "TaskFlow API"}

@app.get("/health")
def get_health():
    return {"status": "ok"}
