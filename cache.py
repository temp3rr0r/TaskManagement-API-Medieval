import redis
import json
import os
from models import Task

# Get Redis URL from environment variable or use default
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

def get_redis_client():
    """Create and return a Redis client"""
    return redis.from_url(REDIS_URL)

def set_cache(redis_client, key, value, expiration=3600):
    """
    Store a value in Redis cache
    
    Args:
        redis_client: Redis client instance
        key: Cache key
        value: Value to cache (SQLAlchemy model instance)
        expiration: Cache expiration time in seconds (default: 1 hour)
    """
    # Convert SQLAlchemy model to dict
    if hasattr(value, "__dict__"):
        value_dict = {
            "id": value.id,
            "title": value.title,
            "description": value.description,
            "status": value.status,
            "createdAt": value.createdAt,
            "updatedAt": value.updatedAt
        }
        redis_client.setex(key, expiration, json.dumps(value_dict))

def get_cache(redis_client, key):
    """
    Retrieve a value from Redis cache
    
    Args:
        redis_client: Redis client instance
        key: Cache key
        
    Returns:
        Cached value or None if not found
    """
    cached_data = redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None

def invalidate_cache(redis_client, key):
    """
    Remove a value from Redis cache
    
    Args:
        redis_client: Redis client instance
        key: Cache key to invalidate
    """
    redis_client.delete(key) 