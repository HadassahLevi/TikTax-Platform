"""
Tik-Tax API - Main Application Entry Point
FastAPI application initialization with middleware, routes, and error handlers
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.exceptions import TikTaxException
from app.api.v1.router import api_router
from app.db.session import engine
from app.middleware.rate_limit import rate_limit_middleware
from app.middleware.error_handler import error_handler_middleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    Handles startup and shutdown tasks
    """
    # Startup
    logger.info("🚀 Starting Tik-Tax API...")
    
    # Test database connection
    try:
        from app.db.session import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        logger.info("✅ Database connection successful")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
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
# So error_handler_middleware wraps everything, including rate limiting

# Rate limiting middleware (applies to all API endpoints)
@app.middleware("http")
async def rate_limit(request: Request, call_next):
    """Apply rate limiting to API requests"""
    return await rate_limit_middleware(request, call_next)


# Global error handler middleware (catches all exceptions)
@app.middleware("http")
async def error_handler(request: Request, call_next):
    """Handle all exceptions globally with Hebrew messages"""
    return await error_handler_middleware(request, call_next)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    logger.info(f"📨 {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        logger.info(f"✅ {request.method} {request.url.path} - {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"❌ {request.method} {request.url.path} - Error: {str(e)}")
        raise


# Exception handlers
@app.exception_handler(TikTaxException)
async def tiktax_exception_handler(request: Request, exc: TikTaxException):
    """Handle custom Tik-Tax exceptions"""
    logger.warning(f"TikTax Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    errors = exc.errors()
    logger.warning(f"Validation Error: {errors}")
    
    # Extract field names from errors
    field_errors = [error.get("loc")[-1] for error in errors]
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Validation failed",
            "hebrew_message": f"שגיאת ולידציה בשדות: {', '.join(field_errors)}",
            "details": errors
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors"""
    logger.error(f"Database Error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Database error occurred",
            "hebrew_message": "אירעה שגיאת מסד נתונים. אנא נסה שוב מאוחר יותר",
            "details": None
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
            "hebrew_message": "אירעה שגיאה בשרת. אנא נסה שוב מאוחר יותר",
            "details": None
        }
    )


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
