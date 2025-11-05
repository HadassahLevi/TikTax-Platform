"""
Tik-Tax API - Main Application Entry Point
FastAPI application initialization with:
- Production-grade logging (JSON structured)
- Error monitoring (Sentry)
- Global exception handling
- Request tracking middleware
- Security middleware
"""

import logging
import uuid
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.exceptions import TikTaxException
from app.core.logging_config import setup_logging
from app.core.monitoring import init_sentry, set_user_context
from app.api.v1.router import api_router
from app.db.session import engine
from app.middleware.rate_limit import rate_limit_middleware
from app.middleware.error_handler import global_exception_handler, tiktax_exception_handler
from app.middleware.audit_log import audit_log_middleware

# Initialize structured logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    Handles startup and shutdown tasks with proper monitoring
    """
    # Startup
    logger.info("🚀 Starting Tik-Tax API...", extra={
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION
    })
    
    # Initialize Sentry monitoring
    init_sentry()
    
    # Test database connection
    try:
        from app.db.session import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("✅ Database connection successful")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}", exc_info=True)
        raise
    
    logger.info("✅ Tik-Tax API started successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Tik-Tax API...")
    engine.dispose()
    logger.info("✅ Database connections closed")


# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add custom middleware
# Note: Middleware is executed in reverse order (bottom to top)

# Request ID and logging middleware
@app.middleware("http")
async def request_tracking_middleware(request: Request, call_next):
    """
    Add request ID and track request duration
    Provides context for structured logging
    """
    # Generate unique request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Track request start time
    start_time = time.time()
    
    # Log incoming request
    logger.info(
        f"📨 {request.method} {request.url.path}",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "ip_address": request.client.host if request.client else None
        }
    )
    
    try:
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = round((time.time() - start_time) * 1000, 2)
        
        # Log response
        logger.info(
            f"✅ {request.method} {request.url.path} - {response.status_code}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms
            }
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response
        
    except Exception as e:
        # Calculate duration even for errors
        duration_ms = round((time.time() - start_time) * 1000, 2)
        
        logger.error(
            f"❌ {request.method} {request.url.path} - Error: {str(e)}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "duration_ms": duration_ms
            },
            exc_info=True
        )
        raise


# Audit logging middleware (logs all API requests)
@app.middleware("http")
async def audit_log(request: Request, call_next):
    """Log all API requests for compliance and debugging"""
    return await audit_log_middleware(request, call_next)


# Rate limiting middleware (applies to all API endpoints)
@app.middleware("http")
async def rate_limit(request: Request, call_next):
    """Apply rate limiting to API requests"""
    return await rate_limit_middleware(request, call_next)

# Register exception handlers
app.add_exception_handler(TikTaxException, tiktax_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)
app.add_exception_handler(SQLAlchemyError, global_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    API root endpoint
    Returns basic API information
    """
    return {
        "name": settings.PROJECT_NAME,
        "name_he": settings.PROJECT_NAME_HE,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "docs": f"{settings.API_V1_STR}/docs",
        "status": "operational"
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    Verifies API and database connectivity
    """
    try:
        from app.db.session import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
