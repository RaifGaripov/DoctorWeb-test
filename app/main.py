import asyncio
import random

from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, HTTPException

from app.db import async_session, init_db
from app.models import Task

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация базы данных перед запуском приложения"""
    await init_db()
    yield


# Максимальное количество обрабатываемых одновременно задач
MAX_TASKS = 2

app = FastAPI(lifespan=lifespan)
semaphore = asyncio.Semaphore(MAX_TASKS)


async def process_task(task_id: int):
    """Обработка задачи"""
    async with semaphore:
        async with async_session() as session:
            task = await session.get(Task, task_id)
            task.status = "Run"
            task.start_time = datetime.now()
            await session.commit()

            # заглушка
            execute_time = random.randint(1, 10)
            await asyncio.sleep(execute_time)

            task.status = "Completed"
            task.time_to_execute = execute_time
            await session.commit()


@app.post("/tasks")
async def create_task(background_tasks: BackgroundTasks):
    """Добавление задачи в очередь"""
    async with async_session() as session:
        task = Task()
        session.add(task)
        await session.commit()
        await session.refresh(task)

        background_tasks.add_task(process_task, task.id)
        return {"task_id": task.id}


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: int):
    """Получение информации о статусе задачи по id"""
    async with async_session() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "status": task.status,
            "create_time": task.create_time.isoformat(),
            "start_time": task.start_time.isoformat() if task.start_time else None,
            "time_to_execute": task.time_to_execute
        }
