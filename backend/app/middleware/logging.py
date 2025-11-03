"""
Request/Response Logging Middleware
Logs all incoming requests and outgoing responses
"""

import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        # Start timer
        start_time = time.time()
        
        # Log request
        logger.info(
            f"📨 {request.method} {request.url.path} "
            f"- Client: {request.client.host if request.client else 'Unknown'}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"✅ {request.method} {request.url.path} "
            f"- Status: {response.status_code} "
            f"- Duration: {duration:.2f}s"
        )
        
        return response
