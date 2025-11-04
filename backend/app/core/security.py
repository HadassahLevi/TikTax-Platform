"""
Tik-Tax Security Utilities
Password hashing, JWT token management, and Israeli validation utilities
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import re
import logging

from .config import settings

logger = logging.getLogger(__name__)

# Password hashing context - NEVER log passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain password against hashed password.
    
    Args:
        plain_password: User-provided password (never logged)
        hashed_password: Stored bcrypt hash
        
    Returns:
        bool: True if password matches
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification failed: {str(e)}")
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password (never logged)
        
    Returns:
        str: Bcrypt hashed password
    """
    return pwd_context.hash(password)


# ============================================================================
# JWT Token Functions
# ============================================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token with configurable expiration.
    
    Args:
        data: Payload data (typically {"sub": user_id})
        expires_delta: Custom expiration time (default from settings)
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "type": "access",
        "iat": datetime.utcnow()  # Issued at
    })
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.info(f"Access token created for user: {data.get('sub')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create access token: {str(e)}")
        raise


def create_refresh_token(data: dict) -> str:
    """
    Create JWT refresh token with long expiration.
    
    Args:
        data: Payload data (typically {"sub": user_id})
        
    Returns:
        str: Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "iat": datetime.utcnow()
    })
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.info(f"Refresh token created for user: {data.get('sub')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create refresh token: {str(e)}")
        raise


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """
    Verify JWT token and return payload if valid.
    
    Args:
        token: JWT token string (never logged in full)
        token_type: Expected token type ("access" or "refresh")
        
    Returns:
        dict: Token payload if valid, None if invalid/expired
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Verify token type
        if payload.get("type") != token_type:
            logger.warning(f"Invalid token type. Expected: {token_type}, Got: {payload.get('type')}")
            return None
        
        # Check expiration (jwt.decode already checks, but explicit is better)
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            logger.info("Token expired")
            return None
        
        return payload
    
    except JWTError as e:
        logger.warning(f"JWT verification failed: {type(e).__name__}")
        return None
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return None


# ============================================================================
# Israeli Validation Utilities
# ============================================================================

def validate_israeli_id(id_number: str) -> bool:
    """
    Validate Israeli ID number using official check digit algorithm.
    
    The Israeli ID is 9 digits with the last digit being a checksum.
    Algorithm: Luhn-like algorithm with alternating weights.
    
    Args:
        id_number: 9-digit Israeli ID number (תעודת זהות)
        
    Returns:
        bool: True if valid ID number
    
    Example:
        >>> validate_israeli_id("123456789")
        False
        >>> validate_israeli_id("000000018")  # Valid test ID
        True
    """
    # Basic validation
    if not id_number or len(id_number) != 9:
        return False
    
    if not id_number.isdigit():
        return False
    
    # Pad with leading zeros if needed (some IDs start with 0)
    id_number = id_number.zfill(9)
    
    # Calculate check digit using Israeli algorithm
    total = 0
    for i, digit in enumerate(id_number[:-1]):  # All digits except last
        num = int(digit)
        
        # Alternate between weight 1 and 2
        if i % 2 == 0:
            total += num
        else:
            temp = num * 2
            # If result is two digits, sum them
            total += temp if temp < 10 else temp - 9
    
    # Check digit should make total divisible by 10
    check_digit = (10 - (total % 10)) % 10
    expected_check_digit = int(id_number[-1])
    
    is_valid = check_digit == expected_check_digit
    
    if not is_valid:
        logger.debug(f"Invalid Israeli ID: checksum mismatch")
    
    return is_valid


def validate_business_number(business_number: str) -> bool:
    """
    Validate Israeli business number (מספר עוסק / ח.פ).
    
    Business numbers in Israel are 9 digits.
    This is a basic validation - full validation would require
    checking against the Israeli Companies Registry API.
    
    Args:
        business_number: 9-digit business number
        
    Returns:
        bool: True if format is valid
    """
    if not business_number:
        return False
    
    # Remove common separators
    business_number = business_number.replace("-", "").replace(" ", "")
    
    # Must be exactly 9 digits
    if len(business_number) != 9 or not business_number.isdigit():
        return False
    
    return True


def validate_israeli_phone(phone: str) -> bool:
    """
    Validate Israeli phone number format.
    
    Accepts:
    - 05XXXXXXXX (10 digits starting with 05)
    - +97250XXXXXXXX (international format)
    - Allows spaces and hyphens
    
    Args:
        phone: Phone number string
        
    Returns:
        bool: True if valid Israeli mobile number
    
    Examples:
        >>> validate_israeli_phone("0501234567")
        True
        >>> validate_israeli_phone("+972-50-123-4567")
        True
        >>> validate_israeli_phone("04-1234567")  # Landline
        False
    """
    if not phone:
        return False
    
    # Remove formatting characters
    clean_phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    
    # Pattern: Israeli mobile number (05X-XXXXXXX)
    # International: +972-5X-XXXXXXX (country code 972)
    pattern = r'^(\+972|0)5[0-9]{8}$'
    
    match = bool(re.match(pattern, clean_phone))
    
    if not match:
        logger.debug(f"Invalid Israeli phone format")
    
    return match


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password meets security requirements.
    
    Requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 digit
    - Optional: Special character (recommended but not required)
    
    Args:
        password: Plain text password (never logged)
        
    Returns:
        tuple: (is_valid: bool, error_message_hebrew: str)
    
    Examples:
        >>> validate_password_strength("weak")
        (False, "הסיסמה חייבת להכיל לפחות 8 תווים")
        >>> validate_password_strength("StrongPass123")
        (True, "")
    """
    if len(password) < 8:
        return False, "הסיסמה חייבת להכיל לפחות 8 תווים"
    
    if not any(c.isupper() for c in password):
        return False, "הסיסמה חייבת להכיל לפחות אות גדולה אחת באנגלית"
    
    if not any(c.islower() for c in password):
        return False, "הסיסמה חייבת להכיל לפחות אות קטנה אחת באנגלית"
    
    if not any(c.isdigit() for c in password):
        return False, "הסיסמה חייבת להכיל לפחות ספרה אחת"
    
    # All validations passed
    return True, ""


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address string
        
    Returns:
        bool: True if valid email format
    """
    if not email:
        return False
    
    # RFC 5322 simplified email pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(pattern, email))
