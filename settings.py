from pydantic_settings import BaseSettings
from typing import Dict
import os

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/taskmanagement")
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    REDIS_CACHE_EXPIRATION: int = 3600  # 1 hour in seconds
    
    # Ollama settings
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL: str = "llama3.2"
    
    # RAG settings
    RAG_NUM_CHUNKS: int = 5  # Number of chunks to retrieve (k)
    RAG_CHUNK_SIZE: int = 1200  # Size of text chunks when splitting documents
    RAG_CHUNK_OVERLAP: int = 300  # Overlap between chunks

    # PDF settings
    PDF_PATH: str = os.getenv("PDF_PATH", "/app/data/knowledge_base.pdf")
    
    # System messages for different contexts
    SYSTEM_MESSAGES: Dict[str, str] = {
        "task_summary": "You are a helpful assistant that summarizes tasks concisely.",
        "knowledge_base": "You are a knowledgeable assistant that provides accurate and relevant information from the knowledge base.",
        "general": "You are a helpful AI assistant focused on task management."
    }
    
    # Task status options
    VALID_TASK_STATUSES: list[str] = ["Pending", "In Progress", "Complete"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create a global settings instance
settings = Settings() 