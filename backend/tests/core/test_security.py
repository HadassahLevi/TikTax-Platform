"""
Unit Tests for Tik-Tax Security Utilities
Tests for password hashing, JWT tokens, and Israeli validators
"""

import pytest
from datetime import datetime, timedelta
from jose import jwt

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
    validate_israeli_id,
    validate_business_number,
    validate_israeli_phone,
    validate_password_strength,
    validate_email
)
from app.core.config import settings


# ============================================================================
# Password Hashing Tests
# ============================================================================

class TestPasswordHashing:
    """Test password hashing and verification"""
    
    def test_password_hash_creates_different_hash(self):
        """Same password should create different hashes (bcrypt includes salt)"""
        password = "MySecurePassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2  # Different salts
        assert hash1.startswith("$2b$")  # Bcrypt format
    
    def test_password_verification_success(self):
        """Correct password should verify successfully"""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_password_verification_failure(self):
        """Wrong password should fail verification"""
        password = "CorrectPassword123"
        wrong_password = "WrongPassword456"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_password_hash_not_plaintext(self):
        """Hash should not contain the original password"""
        password = "MyPassword123"
        hashed = get_password_hash(password)
        
        assert password not in hashed


# ============================================================================
# JWT Token Tests
# ============================================================================

class TestJWTTokens:
    """Test JWT token creation and verification"""
    
    def test_create_access_token(self):
        """Access token should be created with correct claims"""
        user_id = 123
        token = create_access_token(data={"sub": user_id})
        
        # Decode without verification to inspect
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        assert payload["sub"] == user_id
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_create_refresh_token(self):
        """Refresh token should be created with correct claims"""
        user_id = 456
        token = create_refresh_token(data={"sub": user_id})
        
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"
        assert "exp" in payload
    
    def test_verify_valid_access_token(self):
        """Valid access token should verify successfully"""
        user_id = 789
        token = create_access_token(data={"sub": user_id})
        
        payload = verify_token(token, token_type="access")
        
        assert payload is not None
        assert payload["sub"] == user_id
        assert payload["type"] == "access"
    
    def test_verify_valid_refresh_token(self):
        """Valid refresh token should verify successfully"""
        user_id = 101
        token = create_refresh_token(data={"sub": user_id})
        
        payload = verify_token(token, token_type="refresh")
        
        assert payload is not None
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"
    
    def test_verify_token_type_mismatch(self):
        """Access token verified as refresh should fail"""
        user_id = 202
        access_token = create_access_token(data={"sub": user_id})
        
        payload = verify_token(access_token, token_type="refresh")
        
        assert payload is None
    
    def test_verify_expired_token(self):
        """Expired token should fail verification"""
        user_id = 303
        # Create token that expires immediately
        token = create_access_token(
            data={"sub": user_id},
            expires_delta=timedelta(seconds=-1)  # Already expired
        )
        
        payload = verify_token(token, token_type="access")
        
        assert payload is None
    
    def test_verify_invalid_token(self):
        """Invalid token should return None"""
        invalid_token = "invalid.token.string"
        
        payload = verify_token(invalid_token, token_type="access")
        
        assert payload is None
    
    def test_token_custom_expiration(self):
        """Token with custom expiration should respect the delta"""
        user_id = 404
        custom_delta = timedelta(hours=2)
        token = create_access_token(
            data={"sub": user_id},
            expires_delta=custom_delta
        )
        
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        exp_time = datetime.fromtimestamp(payload["exp"])
        iat_time = datetime.fromtimestamp(payload["iat"])
        delta = exp_time - iat_time
        
        # Should be approximately 2 hours (with small tolerance)
        assert abs(delta.total_seconds() - 7200) < 5


# ============================================================================
# Israeli ID Validation Tests
# ============================================================================

class TestIsraeliIDValidation:
    """Test Israeli ID number validation"""
    
    def test_valid_israeli_id(self):
        """Known valid Israeli IDs should pass"""
        valid_ids = [
            "000000018",  # Test ID (checksum 8)
            "123456782",  # Valid checksum
        ]
        
        for id_num in valid_ids:
            assert validate_israeli_id(id_num) is True, f"Failed for {id_num}"
    
    def test_invalid_israeli_id_checksum(self):
        """ID with wrong checksum should fail"""
        assert validate_israeli_id("123456789") is False
    
    def test_israeli_id_wrong_length(self):
        """ID with wrong length should fail"""
        assert validate_israeli_id("12345678") is False  # Too short
        assert validate_israeli_id("1234567890") is False  # Too long
    
    def test_israeli_id_non_numeric(self):
        """ID with non-numeric characters should fail"""
        assert validate_israeli_id("12345678A") is False
        assert validate_israeli_id("12-34-567-89") is False
    
    def test_israeli_id_empty(self):
        """Empty ID should fail"""
        assert validate_israeli_id("") is False
        assert validate_israeli_id(None) is False


# ============================================================================
# Israeli Business Number Validation Tests
# ============================================================================

class TestBusinessNumberValidation:
    """Test Israeli business number validation"""
    
    def test_valid_business_number(self):
        """9-digit number should be valid"""
        assert validate_business_number("512345678") is True
        assert validate_business_number("123456789") is True
    
    def test_business_number_with_separators(self):
        """Business number with separators should be valid after cleaning"""
        assert validate_business_number("51-234-5678") is True
        assert validate_business_number("512 345 678") is True
    
    def test_business_number_wrong_length(self):
        """Business number with wrong length should fail"""
        assert validate_business_number("12345678") is False  # Too short
        assert validate_business_number("1234567890") is False  # Too long
    
    def test_business_number_non_numeric(self):
        """Business number with letters should fail"""
        assert validate_business_number("51234567A") is False
    
    def test_business_number_empty(self):
        """Empty business number should fail"""
        assert validate_business_number("") is False
        assert validate_business_number(None) is False


# ============================================================================
# Israeli Phone Validation Tests
# ============================================================================

class TestIsraeliPhoneValidation:
    """Test Israeli phone number validation"""
    
    def test_valid_israeli_mobile(self):
        """Valid Israeli mobile numbers should pass"""
        valid_phones = [
            "0501234567",
            "0521234567",
            "0531234567",
            "0541234567",
            "0551234567",
        ]
        
        for phone in valid_phones:
            assert validate_israeli_phone(phone) is True, f"Failed for {phone}"
    
    def test_valid_israeli_mobile_international(self):
        """International format should be valid"""
        assert validate_israeli_phone("+972501234567") is True
        assert validate_israeli_phone("+972521234567") is True
    
    def test_israeli_phone_with_separators(self):
        """Phone with separators should be valid"""
        assert validate_israeli_phone("050-123-4567") is True
        assert validate_israeli_phone("+972-50-123-4567") is True
        assert validate_israeli_phone("050 123 4567") is True
    
    def test_israeli_landline_invalid(self):
        """Landline numbers should fail (only mobile accepted)"""
        assert validate_israeli_phone("041234567") is False  # Jerusalem
        assert validate_israeli_phone("031234567") is False  # Tel Aviv
    
    def test_israeli_phone_wrong_format(self):
        """Wrong format should fail"""
        assert validate_israeli_phone("123456789") is False
        assert validate_israeli_phone("0601234567") is False  # Wrong prefix
    
    def test_israeli_phone_empty(self):
        """Empty phone should fail"""
        assert validate_israeli_phone("") is False
        assert validate_israeli_phone(None) is False


# ============================================================================
# Password Strength Validation Tests
# ============================================================================

class TestPasswordStrength:
    """Test password strength validation"""
    
    def test_strong_password(self):
        """Strong password should pass all requirements"""
        is_valid, error = validate_password_strength("StrongPass123")
        assert is_valid is True
        assert error == ""
    
    def test_password_too_short(self):
        """Password shorter than 8 characters should fail"""
        is_valid, error = validate_password_strength("Short1A")
        assert is_valid is False
        assert "8 תווים" in error
    
    def test_password_no_uppercase(self):
        """Password without uppercase should fail"""
        is_valid, error = validate_password_strength("lowercase123")
        assert is_valid is False
        assert "גדולה" in error
    
    def test_password_no_lowercase(self):
        """Password without lowercase should fail"""
        is_valid, error = validate_password_strength("UPPERCASE123")
        assert is_valid is False
        assert "קטנה" in error
    
    def test_password_no_digit(self):
        """Password without digit should fail"""
        is_valid, error = validate_password_strength("NoDigitsHere")
        assert is_valid is False
        assert "ספרה" in error
    
    def test_password_all_requirements_met(self):
        """Password meeting all requirements should pass"""
        strong_passwords = [
            "Password123",
            "MyP@ssw0rd",
            "Secure1Pass",
            "Aa1bcdef",  # Minimal valid
        ]
        
        for password in strong_passwords:
            is_valid, error = validate_password_strength(password)
            assert is_valid is True, f"Failed for {password}: {error}"


# ============================================================================
# Email Validation Tests
# ============================================================================

class TestEmailValidation:
    """Test email format validation"""
    
    def test_valid_emails(self):
        """Valid email formats should pass"""
        valid_emails = [
            "user@example.com",
            "test.user@example.co.il",
            "user+tag@example.com",
            "user123@test-domain.com",
        ]
        
        for email in valid_emails:
            assert validate_email(email) is True, f"Failed for {email}"
    
    def test_invalid_emails(self):
        """Invalid email formats should fail"""
        invalid_emails = [
            "invalid",
            "@example.com",
            "user@",
            "user@domain",
            "user @example.com",
            "",
        ]
        
        for email in invalid_emails:
            assert validate_email(email) is False, f"Should fail for {email}"
    
    def test_email_empty(self):
        """Empty email should fail"""
        assert validate_email("") is False
        assert validate_email(None) is False


# ============================================================================
# Integration Tests
# ============================================================================

class TestSecurityIntegration:
    """Integration tests for security utilities"""
    
    def test_complete_auth_flow(self):
        """Test complete authentication flow"""
        # 1. Hash password
        password = "UserPassword123"
        hashed = get_password_hash(password)
        
        # 2. Verify password
        assert verify_password(password, hashed) is True
        
        # 3. Create access token
        user_id = 999
        access_token = create_access_token(data={"sub": user_id})
        
        # 4. Verify access token
        payload = verify_token(access_token, token_type="access")
        assert payload is not None
        assert payload["sub"] == user_id
        
        # 5. Create refresh token
        refresh_token = create_refresh_token(data={"sub": user_id})
        
        # 6. Verify refresh token
        refresh_payload = verify_token(refresh_token, token_type="refresh")
        assert refresh_payload is not None
        assert refresh_payload["sub"] == user_id
    
    def test_user_signup_validations(self):
        """Test all validations needed for user signup"""
        # Valid data
        email = "user@tiktax.co.il"
        password = "SecurePass123"
        id_number = "123456782"  # Valid Israeli ID
        phone = "0501234567"
        business_number = "512345678"
        
        # Validate all fields
        assert validate_email(email) is True
        is_valid_pass, _ = validate_password_strength(password)
        assert is_valid_pass is True
        assert validate_israeli_id(id_number) is True
        assert validate_israeli_phone(phone) is True
        assert validate_business_number(business_number) is True
