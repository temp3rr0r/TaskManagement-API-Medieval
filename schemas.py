from pydantic import BaseModel, Field
from typing import Optional, List, Dict

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

class KnowledgeQuery(BaseModel):
    """Pydantic model for knowledge base queries"""
    question: str = Field(..., min_length=1, description="The question to ask the knowledge base")

class KnowledgeResponse(BaseModel):
    """Pydantic model for knowledge base responses"""
    answer: str = Field(..., description="The answer from the knowledge base")

class DocumentContent(BaseModel):
    """Pydantic model for a single document's content"""
    filename: str = Field(..., description="Name of the document file")
    content: str = Field(..., description="Content of the document")
    metadata: Dict = Field(default_factory=dict, description="Metadata associated with the document")

class DocumentsResponse(BaseModel):
    """Pydantic model for response containing all document contents"""
    documents: List[DocumentContent] = Field(..., description="List of all parsed documents")
    total_count: int = Field(..., description="Total number of documents") 