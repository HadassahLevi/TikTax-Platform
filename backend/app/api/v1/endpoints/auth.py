"""
Authentication endpoints
Handles user registration, login, token refresh
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, RefreshTokenRequest

router = APIRouter()


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    db: Session = Depends(get_db)
):
    """
    Register new user (3-step process handled by frontend)
    
    Step 1: Email + Password
    Step 2: Personal details
    Step 3: SMS verification
    """
    # TODO: Implement signup logic
    pass


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    User login with email and password
    Returns access and refresh tokens
    """
    # TODO: Implement login logic
    pass


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    # TODO: Implement token refresh logic
    pass


@router.post("/verify-sms")
async def verify_sms(
    phone: str,
    code: str,
    db: Session = Depends(get_db)
):
    """
    Verify SMS code during signup
    """
    # TODO: Implement SMS verification logic
    pass


@router.post("/send-sms")
async def send_sms_code(
    phone: str,
    db: Session = Depends(get_db)
):
    """
    Send SMS verification code
    """
    # TODO: Implement SMS sending logic
    pass
