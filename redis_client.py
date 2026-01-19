import json
import redis
from typing import Optional, Any
from functools import wraps
from fastapi import Request, HTTPException, status
from config import settings

# Redis connection pool
redis_client: Optional[redis.Redis] = None

def get_redis_client() -> Optional[redis.Redis]:
    """Get Redis client instance"""
    global redis_client
    if not settings.redis_enabled:
        return None
    
    if redis_client is None:
        try:
            redis_client = redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            redis_client.ping()
            print("Redis connection established successfully")
        except Exception as e:
            print(f"Redis connection failed: {e}. Continuing without Redis.")
            return None
    return redis_client

def cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate a cache key from prefix and arguments"""
    key_parts = [prefix]
    if args:
        key_parts.extend(str(arg) for arg in args)
    if kwargs:
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    return ":".join(key_parts)

def get_cache(key: str) -> Optional[Any]:
    """Get value from cache"""
    client = get_redis_client()
    if not client:
        return None
    
    try:
        value = client.get(key)
        if value:
            return json.loads(value)
    except Exception as e:
        print(f"Cache get error for key {key}: {e}")
    return None

def set_cache(key: str, value: Any, expire: int = 300) -> bool:
    """Set value in cache with expiration (default 5 minutes)"""
    client = get_redis_client()
    if not client:
        return False
    
    try:
        client.setex(key, expire, json.dumps(value))
        return True
    except Exception as e:
        print(f"Cache set error for key {key}: {e}")
    return False

def delete_cache(key: str) -> bool:
    """Delete a key from cache"""
    client = get_redis_client()
    if not client:
        return False
    
    try:
        client.delete(key)
        return True
    except Exception as e:
        print(f"Cache delete error for key {key}: {e}")
    return False

def delete_cache_pattern(pattern: str) -> int:
    """Delete all keys matching a pattern"""
    client = get_redis_client()
    if not client:
        return 0
    
    try:
        keys = client.keys(pattern)
        if keys:
            return client.delete(*keys)
        return 0
    except Exception as e:
        print(f"Cache delete pattern error for {pattern}: {e}")
    return 0

def cached(expire: int = 300, key_prefix: str = ""):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            if key_prefix:
                cache_key_str = cache_key(key_prefix, *args, **kwargs)
            else:
                cache_key_str = cache_key(func.__name__, *args, **kwargs)
            
            # Try to get from cache
            cached_value = get_cache(cache_key_str)
            if cached_value is not None:
                return cached_value
            
            # Execute function
            result = await func(*args, **kwargs) if hasattr(func, '__await__') else func(*args, **kwargs)
            
            # Store in cache
            set_cache(cache_key_str, result, expire)
            
            return result
        return wrapper
    return decorator

# Rate limiting utilities
def get_client_ip(request: Request) -> str:
    """Extract client IP from request"""
    if request.client:
        return request.client.host
    return "unknown"

def check_rate_limit(key: str, limit: int, window: int = 60) -> tuple[bool, int]:
    """
    Check if rate limit is exceeded
    Returns: (is_allowed, remaining_requests)
    """
    client = get_redis_client()
    if not client:
        return True, limit  # Allow if Redis is unavailable
    
    try:
        current = client.incr(key)
        if current == 1:
            client.expire(key, window)
        
        remaining = max(0, limit - current)
        return current <= limit, remaining
    except Exception as e:
        print(f"Rate limit check error: {e}")
        return True, limit  # Allow if error occurs

def rate_limit(max_requests: int = 10, window: int = 60):
    """Rate limiting decorator"""
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            ip = get_client_ip(request)
            key = f"rate_limit:{func.__name__}:{ip}"
            
            allowed, remaining = check_rate_limit(key, max_requests, window)
            if not allowed:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Maximum {max_requests} requests per {window} seconds.",
                    headers={"X-RateLimit-Remaining": str(remaining)}
                )
            
            # Add rate limit headers
            response = await func(request, *args, **kwargs) if hasattr(func, '__await__') else func(request, *args, **kwargs)
            if hasattr(response, 'headers'):
                response.headers["X-RateLimit-Remaining"] = str(remaining)
                response.headers["X-RateLimit-Limit"] = str(max_requests)
            
            return response
        return wrapper
    return decorator
