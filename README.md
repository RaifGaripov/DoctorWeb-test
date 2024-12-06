# Task Queue API

## Описание проекта

Тестовое задание для вакансии: Программист Python (внутренние проекты) / Python Developer (internal projects)

Прототип веб-сервиса по организации очереди задач с использованием FastAPI, PostgreSQL и SQLAlchemy. Задачи имеют различные статусы выполнения и записываются в базу данных. 

Сервис ограничивает одновременное выполнение задач максимум **двумя** задачами с помощью **asyncio.Semaphore**

## API

- **/tasks** Добавляет задачу в очередь и возвращает её номер.
- **/tasks/{task_id}** Возвращает текущий статус задачи (*In Queue*, *Run*, *Completed*).

## Стэк

- **Python 3.10+**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Docker**

---

## Установка и запуск

### Шаг 1: Склонировать репозиторий
```bash
git clone https://github.com/your-repo/task-queue-api.git
cd task-queue-api
```

## Шаг 2: Создание и запуск Docker-контейнеров

1. Установите и запустите [Docker](https://www.docker.com/)


2. Соберите и запустите контейнеры:
```bash
   docker-compose up --build
```

3. Если контейнер **FastAPI** не запустился (при первом запуске  база данных не успевает проинициализироваться):
   - Проверьте список контейнеров:
     ```bash
     docker ps -a
     ```
   - Запустите контейнер вручную (в отдельной командной строке):
     ```bash
     docker start fastapi_app
     ```
---

## Шаг 3: Использование

После запуска приложение FastAPI предоставляет встроенную документацию по API
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Использование:

1. Создавать задачи с помощью метода `POST /tasks`.
2. Проверять статус задачи по `task_id` через метод `GET /tasks/{task_id}`.

---