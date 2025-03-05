from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    """Base Pydantic model for Task"""
    title: str = Field(..., min_length=1, description="Task title")
    description: str = Field(..., min_length=1, description="Task description")

class TaskCreate(TaskBase):
    """Pydantic model for creating a task"""
    pass

class TaskSummary(BaseModel):
    """Pydantic model for task summary"""
    task_information: str = Field(..., description="Task information")
    task_summary: str = Field(..., description="Task summary")

class TaskUpdate(BaseModel):
    """Pydantic model for updating a task"""
    title: Optional[str] = Field(None, min_length=1, description="Task title")
    description: Optional[str] = Field(None, min_length=1, description="Task description")
    status: Optional[str] = Field(None, description="Task status (Pending, In Progress, Complete)")

class Task(TaskBase):
    """Pydantic model for task response"""
    id: int
    status: str
    createdAt: float
    updatedAt: float

    class Config:
        orm_mode = True 