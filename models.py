from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    CREATED = "создано"
    IN_PROGRESS = "в_работе"
    COMPLETED = "завершено"


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)  # Название
    description: str = Field(..., min_length=1, max_length=500)  # Описание
    status: TaskStatus = TaskStatus.CREATED  # Статус


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)  # Название
    description: str | None = Field(None, min_length=1, max_length=500)  # Описание
    status: TaskStatus | None = None  # Статус


class Task(BaseModel):
    id: UUID  # Идентификатор
    title: str  # Название
    description: str  # Описание
    status: TaskStatus  # Статус