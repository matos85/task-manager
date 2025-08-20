from fastapi import FastAPI, HTTPException, status
from uuid import UUID
from models import Task, TaskCreate, TaskUpdate
from storage import storage

app = FastAPI(title="API Менеджера задач")


@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_create: TaskCreate):
    return storage.create(task_create)


@app.get("/tasks/", response_model=list[Task])
def get_tasks():
    return storage.get_list()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID):
    task = storage.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: TaskUpdate):
    updated_task = storage.update(task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return updated_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID):
    if not storage.delete(task_id):
        raise HTTPException(status_code=404, detail="Задача не найдена")