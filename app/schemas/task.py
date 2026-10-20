from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    completed: bool = False


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime


class TaskChange(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    completed: bool


class TaskPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None

    @field_validator("title", "completed", mode="before")
    @classmethod
    def reject_null_for_required_fields(cls, value):
        if value is None:
            raise ValueError("Field cannot be null")
        return value
