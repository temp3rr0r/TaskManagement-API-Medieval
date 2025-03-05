import os
from pydantic_settings import BaseSettings
from typing import Dict, ClassVar

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/taskmanagement")
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    REDIS_CACHE_EXPIRATION: int = 3600  # 1 hour in seconds
    
    # Ollama settings
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    # Data directory for PDF files
    DATA_DIR: str = os.getenv("DATA_DIR", "/app/data")
    
    # RAG settings
    RAG_NUM_CHUNKS: int = 5  # Number of chunks to retrieve (k)
    RAG_CHUNK_SIZE: int = 1200  # Size of text chunks when splitting documents
    RAG_CHUNK_OVERLAP: int = 300  # Overlap between chunks
    
    # System messages as a class variable (not a field)
    SYSTEM_MESSAGES: ClassVar[Dict[str, str]] = {
        'knowledge_base': 'You are a helpful AI assistant with expertise in historical armour and weapons. Your task is to provide accurate and detailed information based on the provided context. Please be concise but thorough in your responses.',
        'task_summary': 'You are a helpful AI assistant that summarizes task descriptions concisely and professionally.',
        'general': 'You are a helpful AI assistant focused on task management.'
    }
    
    # Task status options
    VALID_TASK_STATUSES: list[str] = ["Pending", "In Progress", "Complete"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create a global settings instance
settings = Settings() 