import os
from pydantic_settings import BaseSettings
from typing import Dict, ClassVar

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/taskmanagement"
    
    # Redis settings
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_CACHE_EXPIRATION: int = 3600  # 1 hour in seconds
    
    # Ollama settings
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2-medieval"
    OLLAMA_EMBEDDING_MODEL: str = "llama3.2-medieval"
    
    # Knowledge base settings
    DATA_DIR: str = "/app/data"
    
    # Additional RAG parameters that were missing
    RAG_TOP_K_RESULTS: int = 3
    RAG_CHUNK_SIZE: int = 1000
    RAG_CHUNK_OVERLAP: int = 200
    
    # Task settings
    VALID_TASK_STATUSES: list = ["Pending", "In Progress", "Complete"]
    
    # System messages for Ollama
    SYSTEM_MESSAGES: dict = {
        "general": "You are a helpful AI assistant focused on task management.",
        "task_summary": "You are a task management assistant. Generate a concise summary of the task.",
        "knowledge_base": "You are a helpful AI assistant with expertise in historical armour and weapons. Your task is to provide accurate and detailed information based on the provided context. Please be concise but thorough in your responses."
    }
    
    # Task status options
    VALID_TASK_STATUSES: list[str] = ["Pending", "In Progress", "Complete"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create a global settings instance
settings = Settings() 