"""
API v1 Main Router
Aggregates all endpoint routers
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, receipts, users, categories, export, subscriptions, statistics

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(receipts.router, prefix="/receipts", tags=["Receipts"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(export.router, prefix="/export", tags=["Export"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["Statistics"])
