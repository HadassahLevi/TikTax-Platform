"""
Authentication endpoints
Handles user registration, login, token refresh, and password management
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from ....db.session import get_db
from ....models.user import User, SubscriptionPlan
from ....schemas.auth import (
    SignupRequest, LoginRequest, TokenResponse, RefreshTokenRequest,
    SendSMSRequest, VerifySMSRequest, ForgotPasswordRequest,
    ResetPasswordRequest, ChangePasswordRequest, UserResponse
)
from ....core.security import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token, verify_token
)
from ....core.config import settings
from ....core.dependencies import get_current_user
from ....core.exceptions import AuthenticationError, ValidationError
from ....services.sms_service import sms_service
from ....services.email_service import email_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/send-verification", status_code=status.HTTP_200_OK)
async def send_sms_verification(
    request: SendSMSRequest,
    db: Session = Depends(get_db)
):
    """
    Send SMS verification code to phone number
    Rate limited: Max 3 requests per hour per phone
    
    Args:
        request: Phone number to send verification code to
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        ValidationError: If phone already registered or SMS sending fails
    """
    # Check if phone already registered
    existing_user = db.query(User).filter(User.phone_number == request.phone_number).first()
    if existing_user and existing_user.is_phone_verified:
        raise ValidationError("מספר טלפון זה כבר רשום במערכת")
    
    # Send SMS
    success = await sms_service.send_verification_code(request.phone_number)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="שגיאה בשליחת SMS. נסה שוב."
        )
    
    return {"message": "קוד אימות נשלח בהצלחה"}


@router.post("/verify-sms", status_code=status.HTTP_200_OK)
async def verify_sms_code(request: VerifySMSRequest):
    """
    Verify SMS code
    
    Args:
        request: Phone number and verification code
        
    Returns:
        Success message
        
    Raises:
        ValidationError: If code is invalid or expired
    """
    is_valid = await sms_service.verify_code(request.phone_number, request.code)
    if not is_valid:
        raise ValidationError("קוד אימות שגוי או פג תוקף")
    
    return {"message": "מספר הטלפון אומת בהצלחה"}


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    User signup with SMS verification
    Creates new user and returns access + refresh tokens
    
    Args:
        request: Signup data including SMS verification code
        background_tasks: Background task manager for sending emails
        db: Database session
        
    Returns:
        Access and refresh tokens
        
    Raises:
        ValidationError: If email/ID already exists or SMS code invalid
    """
    # Check email uniqueness
    if db.query(User).filter(User.email == request.email).first():
        raise ValidationError("כתובת המייל כבר רשומה במערכת")
    
    # Check ID uniqueness
    if db.query(User).filter(User.id_number == request.id_number).first():
        raise ValidationError("תעודת הזהות כבר רשומה במערכת")
    
    # Verify SMS code
    is_verified = await sms_service.verify_code(request.phone_number, request.sms_code)
    if not is_verified:
        raise ValidationError("קוד SMS שגוי או פג תוקף")
    
    # Create user
    user = User(
        email=request.email,
        hashed_password=get_password_hash(request.password),
        full_name=request.full_name,
        id_number=request.id_number,
        phone_number=request.phone_number,
        is_phone_verified=True,
        business_name=request.business_name,
        business_number=request.business_number,
        business_type=request.business_type,
        subscription_plan=SubscriptionPlan.FREE,
        receipt_limit=50,
        receipts_used_this_month=0
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info(f"New user registered: {user.email}")
    
    # Send welcome email in background
    background_tasks.add_task(
        email_service.send_welcome_email,
        user.email,
        user.full_name
    )
    
    # Generate tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    User login with email and password
    Returns access + refresh tokens
    
    Args:
        request: Login credentials
        db: Database session
        
    Returns:
        Access and refresh tokens
        
    Raises:
        AuthenticationError: If credentials invalid or account inactive
    """
    # Find user
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise AuthenticationError("אימייל או סיסמה שגויים")
    
    # Verify password
    if not verify_password(request.password, user.hashed_password):
        raise AuthenticationError("אימייל או סיסמה שגויים")
    
    # Check if account is active
    if not user.is_active:
        raise AuthenticationError("חשבון לא פעיל. צור קשר עם התמיכה.")
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    logger.info(f"User logged in: {user.email}")
    
    # Generate tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    Args:
        request: Refresh token
        db: Database session
        
    Returns:
        New access and refresh tokens
        
    Raises:
        AuthenticationError: If refresh token invalid or user not found
    """
    payload = verify_token(request.refresh_token, token_type="refresh")
    if not payload:
        raise AuthenticationError("רפרש טוקן לא תקין או פג תוקף")
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or not user.is_active:
        raise AuthenticationError("משתמש לא נמצא או חשבון לא פעיל")
    
    # Generate new tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user
    Note: Since tokens are stored client-side only, this is a no-op
    Client must delete tokens
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Success message
    """
    logger.info(f"User logged out: {current_user.email}")
    return {"message": "התנתקת בהצלחה"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Args:
        current_user: Authenticated user
        
    Returns:
        User profile information
    """
    return current_user


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Request password reset link
    Sends email with reset token
    
    Args:
        request: Email address
        background_tasks: Background task manager
        db: Database session
        
    Returns:
        Success message (always, to prevent email enumeration)
    """
    user = db.query(User).filter(User.email == request.email).first()
    
    # Always return success (don't reveal if email exists)
    if user:
        # Generate reset token (valid for 1 hour)
        reset_token = create_access_token(
            data={"sub": user.id, "type": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        
        # Send email in background
        background_tasks.add_task(
            email_service.send_password_reset_email,
            user.email,
            user.full_name,
            reset_token
        )
        
        logger.info(f"Password reset requested for: {user.email}")
    
    return {"message": "אם המייל קיים במערכת, נשלח אליו קישור לאיפוס סיסמה"}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset password using reset token
    
    Args:
        request: Reset token and new password
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        ValidationError: If token invalid or user not found
    """
    payload = verify_token(request.token, token_type="access")
    if not payload or payload.get("type") != "password_reset":
        raise ValidationError("קישור איפוס סיסמה לא תקין או פג תוקף")
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise ValidationError("משתמש לא נמצא")
    
    # Update password
    user.hashed_password = get_password_hash(request.new_password)
    db.commit()
    
    logger.info(f"Password reset for: {user.email}")
    
    return {"message": "הסיסמה שונתה בהצלחה"}


@router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change password for authenticated user
    
    Args:
        request: Current and new password
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        ValidationError: If current password is incorrect
    """
    # Verify current password
    if not verify_password(request.current_password, current_user.hashed_password):
        raise ValidationError("הסיסמה הנוכחית שגויה")
    
    # Update password
    current_user.hashed_password = get_password_hash(request.new_password)
    db.commit()
    
    logger.info(f"Password changed for: {current_user.email}")
    
    return {"message": "הסיסמה שונתה בהצלחה"}

