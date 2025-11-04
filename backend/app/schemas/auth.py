"""
Authentication Pydantic Schemas
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class SignupRequest(BaseModel):
    """User signup request with SMS verification"""
    # Step 1: Personal Info
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2, max_length=100)
    id_number: str = Field(..., min_length=9, max_length=9)
    phone_number: str
    
    # Step 2: Business Info
    business_name: Optional[str] = None
    business_number: Optional[str] = None
    business_type: Optional[str] = None
    
    # Step 3: SMS Verification Code
    sms_code: str = Field(..., min_length=6, max_length=6)
    
    @validator('id_number')
    def validate_id(cls, v):
        from ..core.security import validate_israeli_id
        if not validate_israeli_id(v):
            raise ValueError('תעודת זהות לא תקינה')
        return v
    
    @validator('phone_number')
    def validate_phone(cls, v):
        from ..core.security import validate_israeli_phone
        if not validate_israeli_phone(v):
            raise ValueError('מספר טלפון לא תקין')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        from ..core.security import validate_password_strength
        is_valid, error_msg = validate_password_strength(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v


class LoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response with expiration"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


class SendSMSRequest(BaseModel):
    """Send SMS verification code request"""
    phone_number: str
    
    @validator('phone_number')
    def validate_phone(cls, v):
        from ..core.security import validate_israeli_phone
        if not validate_israeli_phone(v):
            raise ValueError('מספר טלפון לא תקין')
        return v


class VerifySMSRequest(BaseModel):
    """Verify SMS code request"""
    phone_number: str
    code: str = Field(..., min_length=6, max_length=6)


class ForgotPasswordRequest(BaseModel):
    """Forgot password request"""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request"""
    token: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_password(cls, v):
        from ..core.security import validate_password_strength
        is_valid, error_msg = validate_password_strength(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v


class ChangePasswordRequest(BaseModel):
    """Change password request"""
    current_password: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_password(cls, v):
        from ..core.security import validate_password_strength
        is_valid, error_msg = validate_password_strength(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v


class UserResponse(BaseModel):
    """User response model"""
    id: int
    email: str
    full_name: str
    phone_number: str
    is_phone_verified: bool
    business_name: Optional[str]
    business_number: Optional[str]
    subscription_plan: str
    receipt_limit: int
    receipts_used_this_month: int
    created_at: datetime
    
    class Config:
        from_attributes = True
