from uuid import UUID, uuid4
from typing import Dict
from models import Task, TaskCreate, TaskUpdate


class TaskStorage:
    def __init__(self):
        self.tasks: Dict[UUID, Task] = {}  # Хранилище задач

    def create(self, task_create: TaskCreate) -> Task:
        task_id = uuid4()
        task = Task(id=task_id, **task_create.model_dump())
        self.tasks[task_id] = task
        return task

    def get(self, task_id: UUID) -> Task | None:
        return self.tasks.get(task_id)

    def get_list(self) -> list[Task]:
        return list(self.tasks.values())

    def update(self, task_id: UUID, task_update: TaskUpdate) -> Task | None:
        task = self.tasks.get(task_id)
        if task:
            update_data = task_update.model_dump(exclude_unset=True)
            updated_task = task.model_copy(update=update_data)
            self.tasks[task_id] = updated_task
            return updated_task
        return None

    def delete(self, task_id: UUID) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False


storage = TaskStorage()