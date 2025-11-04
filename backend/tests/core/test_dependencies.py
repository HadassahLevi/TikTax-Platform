"""
Unit Tests for FastAPI Dependencies
Tests for authentication and authorization dependencies
"""

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from unittest.mock import Mock, MagicMock
from datetime import datetime

from app.core.dependencies import (
    get_current_user,
    get_current_active_user,
    check_subscription_limit,
    get_current_user_with_subscription_check
)
from app.core.exceptions import AuthenticationError
from app.models.user import User, SubscriptionPlan


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_db():
    """Mock database session"""
    db = MagicMock()
    return db


@pytest.fixture
def mock_valid_token():
    """Mock valid JWT token"""
    return HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="valid.jwt.token"
    )


@pytest.fixture
def mock_invalid_token():
    """Mock invalid JWT token"""
    return HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="invalid.token"
    )


@pytest.fixture
def mock_active_user():
    """Mock active user"""
    user = Mock(spec=User)
    user.id = 1
    user.email = "test@tiktax.co.il"
    user.is_active = True
    user.subscription_plan = SubscriptionPlan.PRO
    user.receipt_limit = 1000
    user.receipts_used_this_month = 50
    return user


@pytest.fixture
def mock_inactive_user():
    """Mock inactive user"""
    user = Mock(spec=User)
    user.id = 2
    user.email = "inactive@tiktax.co.il"
    user.is_active = False
    return user


@pytest.fixture
def mock_user_at_limit():
    """Mock user at receipt limit"""
    user = Mock(spec=User)
    user.id = 3
    user.email = "limited@tiktax.co.il"
    user.is_active = True
    user.subscription_plan = SubscriptionPlan.FREE
    user.receipt_limit = 50
    user.receipts_used_this_month = 50  # At limit
    return user


@pytest.fixture
def mock_business_user():
    """Mock business plan user (unlimited)"""
    user = Mock(spec=User)
    user.id = 4
    user.email = "business@tiktax.co.il"
    user.is_active = True
    user.subscription_plan = SubscriptionPlan.BUSINESS
    user.receipt_limit = 999999
    user.receipts_used_this_month = 5000  # Can use unlimited
    return user


# ============================================================================
# get_current_user Tests
# ============================================================================

class TestGetCurrentUser:
    """Test get_current_user dependency"""
    
    @pytest.mark.asyncio
    async def test_valid_token_returns_user(
        self,
        mock_db,
        mock_valid_token,
        mock_active_user,
        monkeypatch
    ):
        """Valid token should return authenticated user"""
        # Mock verify_token to return valid payload
        def mock_verify_token(token, token_type):
            return {"sub": 1}  # User ID 1
        
        monkeypatch.setattr(
            "app.core.dependencies.verify_token",
            mock_verify_token
        )
        
        # Mock database query
        mock_db.query.return_value.filter.return_value.first.return_value = mock_active_user
        
        # Call dependency
        user = await get_current_user(mock_valid_token, mock_db)
        
        assert user == mock_active_user
        assert user.is_active is True
    
    @pytest.mark.asyncio
    async def test_invalid_token_raises_error(
        self,
        mock_db,
        mock_invalid_token,
        monkeypatch
    ):
        """Invalid token should raise AuthenticationError"""
        # Mock verify_token to return None (invalid)
        def mock_verify_token(token, token_type):
            return None
        
        monkeypatch.setattr(
            "app.core.dependencies.verify_token",
            mock_verify_token
        )
        
        # Should raise AuthenticationError
        with pytest.raises(AuthenticationError) as exc_info:
            await get_current_user(mock_invalid_token, mock_db)
        
        assert "אסימון לא תקין" in str(exc_info.value.hebrew_message)
    
    @pytest.mark.asyncio
    async def test_user_not_found_raises_error(
        self,
        mock_db,
        mock_valid_token,
        monkeypatch
    ):
        """User not in database should raise AuthenticationError"""
        # Mock verify_token to return valid payload
        def mock_verify_token(token, token_type):
            return {"sub": 999}  # Non-existent user
        
        monkeypatch.setattr(
            "app.core.dependencies.verify_token",
            mock_verify_token
        )
        
        # Mock database query to return None (user not found)
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Should raise AuthenticationError
        with pytest.raises(AuthenticationError) as exc_info:
            await get_current_user(mock_valid_token, mock_db)
        
        assert "משתמש לא נמצא" in str(exc_info.value.hebrew_message)
    
    @pytest.mark.asyncio
    async def test_inactive_user_raises_error(
        self,
        mock_db,
        mock_valid_token,
        mock_inactive_user,
        monkeypatch
    ):
        """Inactive user should raise AuthenticationError"""
        # Mock verify_token to return valid payload
        def mock_verify_token(token, token_type):
            return {"sub": 2}  # Inactive user ID
        
        monkeypatch.setattr(
            "app.core.dependencies.verify_token",
            mock_verify_token
        )
        
        # Mock database query to return inactive user
        mock_db.query.return_value.filter.return_value.first.return_value = mock_inactive_user
        
        # Should raise AuthenticationError
        with pytest.raises(AuthenticationError) as exc_info:
            await get_current_user(mock_valid_token, mock_db)
        
        assert "חשבון לא פעיל" in str(exc_info.value.hebrew_message)


# ============================================================================
# get_current_active_user Tests
# ============================================================================

class TestGetCurrentActiveUser:
    """Test get_current_active_user dependency"""
    
    @pytest.mark.asyncio
    async def test_active_user_passes(self, mock_active_user):
        """Active user should pass through"""
        user = await get_current_active_user(mock_active_user)
        assert user == mock_active_user
    
    @pytest.mark.asyncio
    async def test_inactive_user_raises_error(self, mock_inactive_user):
        """Inactive user should raise HTTPException"""
        with pytest.raises(HTTPException) as exc_info:
            await get_current_active_user(mock_inactive_user)
        
        assert exc_info.value.status_code == 403


# ============================================================================
# check_subscription_limit Tests
# ============================================================================

class TestCheckSubscriptionLimit:
    """Test check_subscription_limit function"""
    
    def test_user_within_limit(self, mock_active_user, mock_db):
        """User within limit should pass"""
        # Should not raise exception
        check_subscription_limit(mock_active_user, mock_db)
    
    def test_user_at_limit_raises_error(self, mock_user_at_limit, mock_db):
        """User at limit should raise HTTPException"""
        with pytest.raises(HTTPException) as exc_info:
            check_subscription_limit(mock_user_at_limit, mock_db)
        
        assert exc_info.value.status_code == 402  # Payment required
        assert "מכסת הקבלות" in exc_info.value.detail
    
    def test_business_plan_unlimited(self, mock_business_user, mock_db):
        """Business plan should have unlimited receipts"""
        # Should not raise exception even with high usage
        check_subscription_limit(mock_business_user, mock_db)
    
    def test_user_over_limit_raises_error(self, mock_db):
        """User over limit should raise HTTPException"""
        user = Mock(spec=User)
        user.subscription_plan = SubscriptionPlan.FREE
        user.receipt_limit = 50
        user.receipts_used_this_month = 51  # Over limit
        
        with pytest.raises(HTTPException) as exc_info:
            check_subscription_limit(user, mock_db)
        
        assert exc_info.value.status_code == 402


# ============================================================================
# get_current_user_with_subscription_check Tests
# ============================================================================

class TestGetCurrentUserWithSubscriptionCheck:
    """Test combined dependency with subscription check"""
    
    @pytest.mark.asyncio
    async def test_user_within_limit_passes(self, mock_active_user, mock_db):
        """User within limit should pass all checks"""
        user = await get_current_user_with_subscription_check(
            mock_active_user,
            mock_db
        )
        assert user == mock_active_user
    
    @pytest.mark.asyncio
    async def test_user_at_limit_raises_error(self, mock_user_at_limit, mock_db):
        """User at limit should raise exception"""
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user_with_subscription_check(
                mock_user_at_limit,
                mock_db
            )
        
        assert exc_info.value.status_code == 402
    
    @pytest.mark.asyncio
    async def test_business_user_passes(self, mock_business_user, mock_db):
        """Business user should always pass"""
        user = await get_current_user_with_subscription_check(
            mock_business_user,
            mock_db
        )
        assert user == mock_business_user


# ============================================================================
# Integration Tests
# ============================================================================

class TestDependenciesIntegration:
    """Integration tests for dependencies"""
    
    @pytest.mark.asyncio
    async def test_full_auth_flow(
        self,
        mock_db,
        mock_valid_token,
        mock_active_user,
        monkeypatch
    ):
        """Test complete authentication flow with all dependencies"""
        # Mock verify_token
        def mock_verify_token(token, token_type):
            return {"sub": 1}
        
        monkeypatch.setattr(
            "app.core.dependencies.verify_token",
            mock_verify_token
        )
        
        # Mock database query
        mock_db.query.return_value.filter.return_value.first.return_value = mock_active_user
        
        # 1. Get current user
        user = await get_current_user(mock_valid_token, mock_db)
        assert user == mock_active_user
        
        # 2. Check active status
        active_user = await get_current_active_user(user)
        assert active_user == mock_active_user
        
        # 3. Check subscription limit
        check_subscription_limit(user, mock_db)
        
        # 4. Combined check
        final_user = await get_current_user_with_subscription_check(user, mock_db)
        assert final_user == mock_active_user
