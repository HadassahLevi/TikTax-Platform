"""
Rate Limiting Middleware for Tik-Tax API
Prevents abuse by limiting requests per time period per IP address
"""

from fastapi import Request, HTTPException, status
from typing import Dict
import time
from collections import defaultdict
import logging

from ..core.config import settings

logger = logging.getLogger(__name__)

# In-memory rate limiting storage
# WARNING: This is for development/small-scale deployment only
# PRODUCTION: Replace with Redis-based solution for distributed systems
request_counts: Dict[str, list] = defaultdict(list)


async def rate_limit_middleware(request: Request, call_next):
    """
    Simple rate limiting middleware.
    Tracks requests per IP address and enforces limits.
    
    Flow:
    1. Extract client IP
    2. Clean old request timestamps (>1 minute)
    3. Check if limit exceeded
    4. Add current request if within limit
    5. Process request
    
    Production Replacement:
        Use Redis with sliding window algorithm:
        ```python
        import redis
        redis_client = redis.Redis()
        key = f"rate_limit:{client_ip}"
        count = redis_client.incr(key)
        if count == 1:
            redis_client.expire(key, 60)
        if count > settings.RATE_LIMIT_PER_MINUTE:
            raise HTTPException(429)
        ```
    
    Args:
        request: FastAPI request object
        call_next: Next middleware in chain
        
    Returns:
        Response from next middleware
        
    Raises:
        HTTPException: If rate limit exceeded (429 Too Many Requests)
    """
    # Only apply rate limiting to API endpoints
    if request.url.path.startswith("/api/"):
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean old requests (older than 1 minute)
        request_counts[client_ip] = [
            req_time for req_time in request_counts[client_ip]
            if current_time - req_time < 60
        ]
        
        # Check rate limit
        if len(request_counts[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
            logger.warning(
                f"Rate limit exceeded for IP {client_ip}: "
                f"{len(request_counts[client_ip])} requests in last minute"
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="יותר מדי בקשות. נסה שוב בעוד דקה."
            )
        
        # Add current request timestamp
        request_counts[client_ip].append(current_time)
        
        logger.debug(
            f"IP {client_ip}: {len(request_counts[client_ip])}/{settings.RATE_LIMIT_PER_MINUTE} requests"
        )
    
    # Process request
    response = await call_next(request)
    return response
