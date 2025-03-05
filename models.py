from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.sql import func
import time

from database import Base

class Task(Base):
    """SQLAlchemy model for tasks table"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, default="Pending")
    createdAt = Column(Float, default=time.time)
    updatedAt = Column(Float, default=time.time) 