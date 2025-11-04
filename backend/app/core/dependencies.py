"""
FastAPI Dependencies for Authentication and Authorization
Provides dependency injection for protected routes
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import logging

from ..db.session import get_db
from ..models.user import User
from .security import verify_token
from .exceptions import AuthenticationError

logger = logging.getLogger(__name__)

# HTTP Bearer security scheme (Authorization: Bearer <token>)
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token.
    
    Usage in routes:
        @router.get("/me")
        async def get_me(current_user: User = Depends(get_current_user)):
            return current_user
    
    Args:
        credentials: HTTP Bearer token from Authorization header
        db: Database session
        
    Returns:
        User: Authenticated user object
        
    Raises:
        AuthenticationError: If token is invalid or user not found
    """
    token = credentials.credentials
    payload = verify_token(token, token_type="access")
    
    if payload is None:
        logger.warning("Invalid or expired access token")
        raise AuthenticationError("אסימון לא תקין או פג תוקף")
    
    user_id: int = payload.get("sub")
    if user_id is None:
        logger.warning("Token missing 'sub' claim")
        raise AuthenticationError("אסימון לא תקין")
    
    # Fetch user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.warning(f"User not found in database: {user_id}")
        raise AuthenticationError("משתמש לא נמצא")
    
    if not user.is_active:
        logger.warning(f"Inactive user attempted access: {user_id}")
        raise AuthenticationError("חשבון לא פעיל")
    
    logger.info(f"User authenticated successfully: {user.email}")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure user is active.
    
    This is a stricter version of get_current_user that double-checks
    the user's active status (get_current_user already checks this,
    but this is kept for explicit clarity).
    
    Args:
        current_user: User from get_current_user dependency
        
    Returns:
        User: Active user object
        
    Raises:
        HTTPException: If user is not active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="חשבון לא פעיל"
        )
    return current_user


def check_subscription_limit(user: User, db: Session) -> None:
    """
    Check if user has exceeded their receipt limit for the month.
    
    This is called before processing a new receipt to ensure the user
    has not exceeded their subscription plan's monthly limit.
    
    Args:
        user: User object to check
        db: Database session (for potential future use)
        
    Raises:
        HTTPException: If user has reached their receipt limit
        
    Example:
        check_subscription_limit(current_user, db)
        # Proceed with receipt processing if no exception raised
    """
    # Business plan has unlimited receipts
    if user.subscription_plan.value == "business":
        logger.info(f"User {user.email} has unlimited receipts (business plan)")
        return
    
    # Check if user has exceeded limit
    if user.receipts_used_this_month >= user.receipt_limit:
        logger.warning(
            f"User {user.email} exceeded receipt limit: "
            f"{user.receipts_used_this_month}/{user.receipt_limit}"
        )
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"הגעת למכסת הקבלות החודשית ({user.receipt_limit}). שדרג את המנוי שלך."
        )
    
    logger.info(
        f"User {user.email} within limit: "
        f"{user.receipts_used_this_month}/{user.receipt_limit}"
    )


async def get_current_user_with_subscription_check(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that gets current user AND checks subscription limits.
    
    Use this for receipt processing endpoints that consume the monthly quota.
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        User: Authenticated user who hasn't exceeded limits
        
    Raises:
        HTTPException: If subscription limit reached
    """
    check_subscription_limit(current_user, db)
    return current_user
    
    return user
