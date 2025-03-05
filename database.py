from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
from sqlalchemy.exc import OperationalError

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/taskmanagement")

def get_engine(retries=5, delay=2):
    """Create database engine with retry logic"""
    for i in range(retries):
        try:
            engine = create_engine(DATABASE_URL)
            # Test the connection
            engine.connect()
            return engine
        except OperationalError as e:
            if i == retries - 1:  # Last retry
                raise e
            time.sleep(delay)  # Wait before retrying
            print(f"Retrying database connection... Attempt {i + 2}/{retries}")

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 