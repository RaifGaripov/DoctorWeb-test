import random
import time
import threading

from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException

from app.db import async_session, init_db
from app.models import Task
from app.db import engine

from sqlalchemy.orm import sessionmaker

task_queue = deque()
queue_lock = threading.Lock()


def process_task(task_id: int):
    """Синхронная обработка задачи"""
    with sessionmaker(bind=engine.sync_engine)() as session:
        with queue_lock:
            task = session.get(Task, task_id)
            if not task:
                return

            task.status = "Run"
            task.start_time = datetime.now()
            session.commit()

        # заглушка
        execute_time = random.randint(1, 10)
        time.sleep(execute_time)

        with queue_lock:
            task.status = "Completed"
            task.time_to_execute = execute_time
            session.commit()


def task_worker():
    """Воркер выполняет задачи поочередно по мере поступления"""
    while True:
        with queue_lock:
            if not task_queue:
                continue
            task_id = task_queue.popleft()

        process_task(task_id)


worker_threads = []

# Максимальное количество обрабатываемых одновременно задач
MAX_TASKS = 2
for _ in range(MAX_TASKS):
    thread = threading.Thread(target=task_worker, daemon=True)
    thread.start()
    worker_threads.append(thread)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация базы данных перед запуском приложения"""
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/tasks")
async def create_task():
    """Добавление задачи в очередь"""
    async with async_session() as session:
        task = Task()
        session.add(task)
        await session.commit()
        await session.refresh(task)

        with queue_lock:
            task_queue.append(task.id)

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
