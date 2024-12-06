from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    create_time = Column(DateTime, default=datetime.now())
    start_time = Column(DateTime, nullable=True)
    time_to_execute = Column(Integer, nullable=True)
    status = Column(String, default="In Queue")
