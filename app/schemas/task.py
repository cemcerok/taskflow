from pydantic import BaseModel, Field, ConfigDict


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    completed: bool = False

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool

class TaskChange(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    completed: bool

class TaskPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    completed: bool | None = None
