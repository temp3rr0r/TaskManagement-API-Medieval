from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
import time

from database import get_db
from models import Task as TaskModel
from schemas import Task, TaskCreate, TaskUpdate
from cache import get_redis_client, set_cache, get_cache, invalidate_cache

app = FastAPI(title="Task Management API")

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    db_task = TaskModel(
        title=task.title,
        description=task.description,
        status="Pending"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks", response_model=List[Task])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all tasks"""
    tasks = db.query(TaskModel).offset(skip).limit(limit).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific task by ID with Redis caching"""
    # Try to get task from cache
    redis_client = get_redis_client()
    cached_task = get_cache(redis_client, f"task:{task_id}")
    
    if cached_task:
        return cached_task
    
    # If not in cache, get from database
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Store in cache
    set_cache(redis_client, f"task:{task_id}", db_task)
    
    return db_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task"""
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task fields if provided
    if task.title is not None:
        db_task.title = task.title
    if task.description is not None:
        db_task.description = task.description
    if task.status is not None:
        if task.status not in ["Pending", "In Progress", "Complete"]:
            raise HTTPException(status_code=400, detail="Invalid status value")
        db_task.status = task.status
    
    # Update the updatedAt timestamp
    db_task.updatedAt = time.time()
    
    db.commit()
    db.refresh(db_task)
    
    # Invalidate cache
    redis_client = get_redis_client()
    invalidate_cache(redis_client, f"task:{task_id}")
    
    return db_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    
    # Invalidate cache
    redis_client = get_redis_client()
    invalidate_cache(redis_client, f"task:{task_id}")
    
    return None 