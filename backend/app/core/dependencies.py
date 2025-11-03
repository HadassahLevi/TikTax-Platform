"""
Common dependencies for FastAPI routes
Used for dependency injection
"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import decode_token, verify_token_type
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.db.session import SessionLocal

# HTTP Bearer token security scheme
security = HTTPBearer()


def get_db() -> Generator:
    """
    Database session dependency
    Yields a database session and closes it after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Extract and validate current user ID from JWT token
    
    Args:
        credentials: HTTP Authorization credentials
        
    Returns:
        User ID from token
        
    Raises:
        AuthenticationError: If token is invalid or missing
    """
    token = credentials.credentials
    
    # Decode token
    payload = decode_token(token)
    if payload is None:
        raise AuthenticationError(
            message="Invalid token",
            hebrew_message="טוקן לא תקין. אנא התחבר מחדש"
        )
    
    # Verify token type
    if not verify_token_type(payload, "access"):
        raise AuthenticationError(
            message="Invalid token type",
            hebrew_message="סוג טוקן לא תקין"
        )
    
    # Extract user ID
    user_id: str = payload.get("sub")
    if user_id is None:
        raise AuthenticationError(
            message="Token missing user ID",
            hebrew_message="טוקן חסר מזהה משתמש"
        )
    
    return user_id


async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user from database
    
    Args:
        user_id: User ID from token
        db: Database session
        
    Returns:
        User model instance
        
    Raises:
        AuthenticationError: If user not found
    """
    from app.models.user import User
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise AuthenticationError(
            message="User not found",
            hebrew_message="משתמש לא נמצא במערכת"
        )
    
    if not user.is_active:
        raise AuthorizationError(
            message="Inactive user",
            hebrew_message="חשבון המשתמש אינו פעיל"
        )
    
    return user


async def get_current_active_subscription(
    user = Depends(get_current_user)
):
    """
    Verify user has active subscription
    
    Args:
        user: Current user
        
    Returns:
        User if subscription is active
        
    Raises:
        AuthorizationError: If subscription is not active
    """
    from app.core.exceptions import SubscriptionError
    
    if not user.subscription or not user.subscription.is_active:
        raise SubscriptionError(
            message="No active subscription",
            hebrew_message="אין מנוי פעיל. אנא חדש את המנוי שלך"
        )
    
    return user
