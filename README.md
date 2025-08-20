# Task Manager API

Task Manager API — это бэкенд-приложение на основе **FastAPI** для управления задачами с поддержкой CRUD-операций. Каждая задача имеет UUID, название, описание (с поддержкой Markdown) и статус (`создано`, `в_работе`, `завершено`). Проект включает тесты на **pytest**, документацию Swagger, поддержку **Docker** и соответствует стандартам **PEP8**.

## Основные возможности

- **CRUD-операции**:
  - `POST /tasks/` — Создание задачи
  - `GET /tasks/` — Получение списка задач
  - `GET /tasks/{task_id}` — Получение задачи по UUID
  - `PUT /tasks/{task_id}` — Обновление задачи
  - `DELETE /tasks/{task_id}` — Удаление задачи
- **Модель задачи**:
  - `id`: UUID
  - `title`: строка (1–100 символов)
  - `description`: строка (1–500 символов, поддерживает Markdown)
  - `description_html`: HTML-рендеринг описания
  - `status`: перечисление (`создано`, `в_работе`, `завершено`)
- **Markdown**: Поле `description` поддерживает Markdown (заголовки, списки, полужирный текст, курсив), преобразуемый в HTML.
- **Технологии**:
  - Backend: FastAPI
  - Тестирование: pytest
  - Рендеринг Markdown: библиотека `markdown`
  - Хранилище: In-memory (для продакшена — PostgreSQL)
  - Документация: Swagger UI
  - Контейнеризация: Docker

## Структура проекта
task-manager/
├── main.py              # Точка входа FastAPI
├── models.py            # Pydantic-модели и перечисление статусов
├── storage.py           # In-memory хранилище задач
├── tests/
│   ├── __init__.py      # Пустой файл для модуля
│   ├── test_api.py      # Тесты для всех эндпоинтов
├── requirements.txt     # Зависимости
├── Dockerfile           # Конфигурация Docker
├── pytest.ini           # Конфигурация pytest
├── README.md            # Документация


## Требования

- Python 3.12+
- Docker (опционально)
- Postman или Swagger UI (для ручного тестирования)

## Установка

### Локальная установка

1. Клонируйте репозиторий или создайте файлы:

    ```bash
    git clone <repository-url>
    cd task-manager


Создайте и активируйте виртуальное окружение:
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# Linux/Mac
source .venv/bin/activate


Установите зависимости:pip install -r requirements.txt


Запустите приложение:uvicorn main:app --host 0.0.0.0 --port 8000 --reload


Откройте Swagger UI: http://127.0.0.1:8000/docs

Установка с Docker

Соберите Docker-образ:docker build -t task-manager .


Запустите контейнер:docker run -p 8000:8000 task-manager


Откройте Swagger UI: http://127.0.0.1:8000/docs

Тестирование
Автоматическое тестирование с pytest
Проект включает 12 тестов, покрывающих все CRUD-операции, краевые случаи (например, несуществующие задачи) и валидацию данных.

Активируйте виртуальное окружение:# Windows
.venv\Scripts\Activate.ps1
# Linux/Mac
source .venv/bin/activate


Убедитесь, что файл pytest.ini присутствует в корне проекта:[pytest]
python_paths = .


Запустите тесты из корневой директории проекта:cd task-manager
python -m pytest

Для подробного вывода:python -m pytest -v


Ожидаемый результат:
============================= test session starts =======================
collected 13 items

tests/test_api.py ............. [100%]

========================== 13 passed in X.XXs ==========================


Устранение ошибок
Если вы видите ошибку ModuleNotFoundError: No module named 'main', убедитесь, что:

Вы находитесь в корневой директории проекта (task-manager).
Файл pytest.ini присутствует.
Все файлы (main.py, models.py, storage.py) находятся в корне проекта.
Зависимости установлены (pip install -r requirements.txt).

Ручное тестирование с Postman
Для проверки API используйте Postman или Swagger UI. Ниже описаны запросы для Postman. Создайте коллекцию Task Manager API и настройте переменную base_url (значение: http://127.0.0.1:8000).
1. POST /tasks/ — Создать задачу

Метод: POST
URL: {{base_url}}/tasks/
Заголовки:Content-Type: application/json


Тело запроса (JSON):{
  "title": "Тестовая задача",
  "description": "Описание тестовой задачи",
  "status": "создано"
}


Ожидаемый ответ:
Код: 201 Created
Тело (пример):{
  "id": "<уникальный-uuid>",
  "title": "Тестовая задача",
  "description": "Описание тестовой задачи",
  "status": "создано"
}




Postman-скрипт (вкладка Tests для сохранения task_id):pm.environment.set("task_id", pm.response.json().id);



2. GET /tasks/ — Получить список задач

Метод: GET
URL: {{base_url}}/tasks/
Заголовки: Не требуется
Тело: Отсутствует
Ожидаемый ответ:
Код: 200 OK
Тело (пример):[
  {
    "id": "<уникальный-uuid>",
    "title": "Тестовая задача",
    "description": "Описание тестовой задачи",
    "status": "создано"
  }
]





3. GET /tasks/{task_id} — Получить задачу по UUID

Метод: GET
URL: {{base_url}}/tasks/{{task_id}}
Заголовки: Не требуется
Тело: Отсутствует
Ожидаемый ответ:
Код: 200 OK
Тело (пример):{
  "id": "<уникальный-uuid>",
  "title": "Тестовая задача",
  "description": "Описание тестовой задачи",
  "status": "создано"
}


Если задача не найдена: 404 Not Found с {"detail": "Задача не найдена"}



4. PUT /tasks/{task_id} — Обновить задачу

Метод: PUT
URL: {{base_url}}/tasks/{{task_id}}
Заголовки:Content-Type: application/json


Тело запроса (JSON, можно обновить только часть полей):{
  "title": "Обновленная задача",
  "status": "в_работе"
}


Ожидаемый ответ:
Код: 200 OK
Тело (пример):{
  "id": "<уникальный-uuid>",
  "title": "Обновленная задача",
  "description": "Описание тестовой задачи",
  "status": "в_работе"
}


Если задача не найдена: 404 Not Found



5. DELETE /tasks/{task_id} — Удалить задачу

Метод: DELETE
URL: {{base_url}}/tasks/{{task_id}}
Заголовки: Не требуется
Тело: Отсутствует
Ожидаемый ответ:
Код: 204 No Content (без тела)
Если задача не найдена: 404 Not Found с {"detail": "Задача не найдена"}



Советы по Postman

Используйте переменные {{base_url}} и {{task_id}} для упрощения.
Тестируйте краевые случаи (например, неверный статус или несуществующий UUID).
Для удобства экспортируйте коллекцию Postman и сохраните её в проекте.

Использование API

Swagger UI: Интерактивная документация доступна по http://127.0.0.1:8000/docs. Используйте её для тестирования без Postman.
Создание задач: Используйте POST для добавления задач с уникальными данными.
Обновление: PUT позволяет обновлять поля частично или полностью.
Удаление: DELETE удаляет задачу по UUID.
Список задач: GET /tasks/ возвращает все задачи.

Замечания по качеству

PEP8: Код отформатирован с помощью black/flake8.
Чистый код: Модульная структура, аннотации типов, читаемые имена.
Тесты: 100% покрытие эндпоинтов, включая краевые случаи и валидацию.
Хранилище: In-memory для простоты. Для продакшена используйте PostgreSQL + SQLAlchemy.
Документация: Swagger UI по /docs и данный README.

Устранение неполадок

Ошибка pytest ModuleNotFoundError:
Убедитесь, что запускаете python -m pytest из корня проекта.
Проверьте наличие pytest.ini и файлов main.py, models.py, storage.py.
Установите зависимости: pip install -r requirements.txt.


Ошибка FastAPI: Проверьте, что порт 8000 свободен, и используйте --reload только для разработки.
Docker: Убедитесь, что Docker запущен, и порт 8000 не занят.

Лицензия
MIT License. См. файл LICENSE (если добавлен в проект).
