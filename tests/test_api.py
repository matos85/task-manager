import pytest
from fastapi.testclient import TestClient
from main import app
from models import TaskCreate, TaskStatus, TaskUpdate
from storage import storage
from uuid import uuid4


@pytest.fixture
def client():
    # Сброс хранилища перед каждым тестом
    storage.tasks = {}
    return TestClient(app)


def test_create_task(client):
    task_data = {"title": "Тестовая задача", "description": "Тестовое описание", "status": "создано"}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Тестовая задача"
    assert data["description"] == "Тестовое описание"
    assert data["status"] == "создано"


def test_get_tasks_empty(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_with_data(client):
    task_create = TaskCreate(title="Задача1", description="Описание1")
    task = storage.create(task_create)
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == str(task.id)


def test_get_task(client):
    task_create = TaskCreate(title="Задача2", description="Описание2")
    task = storage.create(task_create)
    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(task.id)
    assert data["title"] == "Задача2"


def test_get_task_not_found(client):
    fake_id = uuid4()
    response = client.get(f"/tasks/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Задача не найдена"


def test_update_task(client):
    task_create = TaskCreate(title="Задача3", description="Описание3", status=TaskStatus.CREATED)
    task = storage.create(task_create)
    update_data = {"title": "Обновленное название", "status": "в_работе"}
    response = client.put(f"/tasks/{task.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Обновленное название"
    assert data["description"] == "Описание3"  # Не изменено
    assert data["status"] == "в_работе"


def test_update_task_partial(client):
    task_create = TaskCreate(title="Задача4", description="Описание4")
    task = storage.create(task_create)
    update_data = {"description": "Обновленное описание"}
    response = client.put(f"/tasks/{task.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Задача4"
    assert data["description"] == "Обновленное описание"


def test_update_task_not_found(client):
    fake_id = uuid4()
    update_data = {"title": "Неудача"}
    response = client.put(f"/tasks/{fake_id}", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Задача не найдена"


def test_delete_task(client):
    task_create = TaskCreate(title="Задача5", description="Описание5")
    task = storage.create(task_create)
    response = client.delete(f"/tasks/{task.id}")
    assert response.status_code == 204
    # Проверка удаления
    get_response = client.get(f"/tasks/{task.id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    fake_id = uuid4()
    response = client.delete(f"/tasks/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Задача не найдена"


def test_invalid_status_create(client):
    task_data = {"title": "Недопустимая", "description": "Описание", "status": "недопустимый_статус"}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 422  # Невозможно обработать


def test_invalid_status_update(client):
    task_create = TaskCreate(title="Задача6", description="Описание6")
    task = storage.create(task_create)
    update_data = {"status": "недопустимый"}
    response = client.put(f"/tasks/{task.id}", json=update_data)
    assert response.status_code == 422


def test_empty_title_create(client):
    task_data = {"title": "", "description": "Описание", "status": "создано"}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 422