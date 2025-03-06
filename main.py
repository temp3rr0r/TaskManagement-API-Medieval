from typing import List, Optional
import time
import os
from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from models import Task as TaskModel
from schemas import Task, TaskCreate, TaskUpdate, TaskSummary, KnowledgeQuery, KnowledgeResponse, DocumentsResponse, DocumentContent
from cache import get_redis_client, set_cache, get_cache, invalidate_cache
import ollama
from rag import rag_manager
from settings import settings

app = FastAPI(title="Task Management API")

def generate_task_summary(task_description: str) -> str:
    """
    Generate a summary of a task using Ollama's LLM
    """
    try:
        ollama.host = settings.OLLAMA_HOST
        
        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": settings.SYSTEM_MESSAGES["task_summary"]
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following task description in a few sentences: {task_description}"
                }
            ]
        )

        return response['message']['content']
    except Exception as e:
        print(f"Error generating task summary: {e}")
        return "Unable to connect to Ollama service. Please try again later."


@app.get("/tasks", response_model=List[Task])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all tasks"""
    tasks = db.query(TaskModel).offset(skip).limit(limit).all()
    return tasks

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
        if task.status not in settings.VALID_TASK_STATUSES:
            raise HTTPException(status_code=400, detail=f"Invalid status value. Must be one of: {', '.join(settings.VALID_TASK_STATUSES)}")
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


@app.get("/tasks/{task_id}/summary", response_model=TaskSummary)
def get_task_summary(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific task by ID with Redis caching. Get a summary of the task."""
    # Try to get task from cache
    redis_client = get_redis_client()
    cached_task = get_cache(redis_client, f"task:{task_id}")

    # TODO: Show all keys from Redis
    print(f"------------------------------ Redis keys: {redis_client.keys()}")
    
    if cached_task:
        db_task = cached_task
        task_information = f'Task ID: {db_task["id"]}. Title: {db_task["title"]}. Description: {db_task["description"]}. Status: {db_task["status"]}. Created at {db_task["createdAt"]} and updated at {db_task["updatedAt"]}.'
        print(f"------------------------------ Task retrieved from Redis: {db_task}")
    else:    
        # If not in cache, get from database
        db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        print(f"------------------------------ Task retrieved from database: {db_task}")
        task_information = f'Task ID: {db_task.id}. Title: {db_task.title}. Description: {db_task.description}. Status: {db_task.status}. Created at {db_task.createdAt} and updated at {db_task.updatedAt}.'
        
    
    str_task_summary = generate_task_summary(task_description=task_information)
    
    task_summary = TaskSummary(task_information=task_information, task_summary=str_task_summary)
    
    return task_summary

        
@app.get("/tasks/{task_id}/knowledge/hints", response_model=TaskSummary)
def get_knowledge_task_hints(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific task by ID with Redis caching. Get a summary of the task using RAG."""
    # Try to get task from cache
    redis_client = get_redis_client()
    cached_task = get_cache(redis_client, f"task:{task_id}")
    
    if cached_task:
        db_task = cached_task
        task_information = f'Task ID: {db_task["id"]}. Title: {db_task["title"]}. Description: {db_task["description"]}. Status: {db_task["status"]}. Created at {db_task["createdAt"]} and updated at {db_task["updatedAt"]}.'
        print(f"------------------------------ Task retrieved from Redis: {db_task}")
    else:    
        # If not in cache, get from database
        db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        print(f"------------------------------ Task retrieved from database: {db_task}")
        task_information = f'Task ID: {db_task.id}. Title: {db_task.title}. Description: {db_task.description}. Status: {db_task.status}. Created at {db_task.createdAt} and updated at {db_task.updatedAt}.'
    
        
    # Get summary of the task
    
    query = KnowledgeQuery(question=f"Please provide hints for the following task, comprehensively and in detail. {task_information}")

    try:
        answer = rag_manager.query_knowledge_base(query.question)

        knowledge_task_hints = TaskSummary(task_information=task_information, task_summary=answer)
        
        return knowledge_task_hints
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing knowledge query: {str(e)}"
        ) 

    
@app.post("/query", response_model=KnowledgeResponse)
def query(query: KnowledgeQuery):
    """
    Query the LLM.
    """
    try:
        ollama.host = settings.OLLAMA_HOST
        
        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": settings.SYSTEM_MESSAGES["general"]
                },
                {
                    "role": "user",
                    "content": f"Please answer the following question: {query.question}"
                }
            ]
        )

        answer = response['message']['content']
        return KnowledgeResponse(answer=answer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )     
    


@app.post("/knowledge/query", response_model=KnowledgeResponse)
def query_knowledge_base(query: KnowledgeQuery):
    """
    Query the LLM and the knowledge base using RAG with the local PDF/EPUB files.
    """
    try:
        answer = rag_manager.query_knowledge_base(query.question)
        return KnowledgeResponse(answer=answer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing knowledge query: {str(e)}"
        )     
    
@app.get("/knowledge/documents", response_model=DocumentsResponse)
def get_documents():
    """
    Retrieve all parsed document contents from the knowledge base.
    """
    try:

        documents = rag_manager.get_all_documents()

        # Format the documents into the response schema
        document_contents = []
        for doc in documents:
            document_content = DocumentContent(
                filename=doc.metadata.get('source', 'Unknown'),
                content=doc.page_content,
                metadata=doc.metadata
            )
            document_contents.append(document_content)
        
        # Create and return the response
        return DocumentsResponse(
            documents=document_contents,
            total_count=len(document_contents)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving document contents: {str(e)}"
        )

