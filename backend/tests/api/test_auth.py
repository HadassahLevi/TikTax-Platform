"""
Unit tests for authentication endpoints
Tests signup, login, token refresh, and password management
"""

import pytest
from fastapi import status
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from app.models.user import User, SubscriptionPlan
from app.core.security import get_password_hash, create_access_token


class TestSendSMSVerification:
    """Test SMS verification code sending"""
    
    @patch('app.services.sms_service.sms_service.send_verification_code')
    def test_send_sms_success(self, mock_send_sms, client, db_session):
        """Test successful SMS sending"""
        mock_send_sms.return_value = True
        
        response = client.post(
            "/api/v1/auth/send-verification",
            json={"phone_number": "+972501234567"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "קוד אימות נשלח בהצלחה" in response.json()["message"]
        mock_send_sms.assert_called_once_with("+972501234567")
    
    def test_send_sms_already_registered(self, client, db_session):
        """Test SMS sending to already registered phone"""
        # Create verified user
        user = User(
            email="test@test.com",
            hashed_password=get_password_hash("password123"),
            full_name="Test User",
            id_number="123456789",
            phone_number="+972501234567",
            is_phone_verified=True,
            subscription_plan=SubscriptionPlan.FREE,
            receipt_limit=50
        )
        db_session.add(user)
        db_session.commit()
        
        response = client.post(
            "/api/v1/auth/send-verification",
            json={"phone_number": "+972501234567"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "כבר רשום במערכת" in response.json()["detail"]
    
    def test_send_sms_invalid_phone(self, client):
        """Test SMS sending with invalid phone format"""
        response = client.post(
            "/api/v1/auth/send-verification",
            json={"phone_number": "invalid"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestVerifySMS:
    """Test SMS code verification"""
    
    @patch('app.services.sms_service.sms_service.verify_code')
    def test_verify_sms_success(self, mock_verify, client):
        """Test successful SMS verification"""
        mock_verify.return_value = True
        
        response = client.post(
            "/api/v1/auth/verify-sms",
            json={
                "phone_number": "+972501234567",
                "code": "123456"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "אומת בהצלחה" in response.json()["message"]
    
    @patch('app.services.sms_service.sms_service.verify_code')
    def test_verify_sms_invalid_code(self, mock_verify, client):
        """Test SMS verification with invalid code"""
        mock_verify.return_value = False
        
        response = client.post(
            "/api/v1/auth/verify-sms",
            json={
                "phone_number": "+972501234567",
                "code": "999999"
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "קוד אימות שגוי" in response.json()["detail"]


class TestSignup:
    """Test user signup"""
    
    @patch('app.services.sms_service.sms_service.verify_code')
    @patch('app.services.email_service.email_service.send_welcome_email')
    def test_signup_success(self, mock_email, mock_sms, client, db_session):
        """Test successful user signup"""
        mock_sms.return_value = True
        mock_email.return_value = True
        
        signup_data = {
            "email": "newuser@test.com",
            "password": "SecurePass123!",
            "full_name": "New User",
            "id_number": "123456789",
            "phone_number": "+972501234567",
            "business_name": "My Business",
            "business_number": "987654321",
            "business_type": "עוסק מורשה",
            "sms_code": "123456"
        }
        
        response = client.post("/api/v1/auth/signup", json=signup_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] > 0
        
        # Verify user created in database
        user = db_session.query(User).filter(User.email == "newuser@test.com").first()
        assert user is not None
        assert user.full_name == "New User"
        assert user.is_phone_verified is True
    
    def test_signup_duplicate_email(self, client, db_session):
        """Test signup with duplicate email"""
        # Create existing user
        user = User(
            email="existing@test.com",
            hashed_password=get_password_hash("password123"),
            full_name="Existing User",
            id_number="123456789",
            phone_number="+972501234567",
            is_phone_verified=True,
            subscription_plan=SubscriptionPlan.FREE,
            receipt_limit=50
        )
        db_session.add(user)
        db_session.commit()
        
        signup_data = {
            "email": "existing@test.com",
            "password": "SecurePass123!",
            "full_name": "New User",
            "id_number": "987654321",
            "phone_number": "+972509999999",
            "sms_code": "123456"
        }
        
        response = client.post("/api/v1/auth/signup", json=signup_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "כבר רשומה במערכת" in response.json()["detail"]
    
    @patch('app.services.sms_service.sms_service.verify_code')
    def test_signup_invalid_sms_code(self, mock_sms, client):
        """Test signup with invalid SMS code"""
        mock_sms.return_value = False
        
        signup_data = {
            "email": "newuser@test.com",
            "password": "SecurePass123!",
            "full_name": "New User",
            "id_number": "123456789",
            "phone_number": "+972501234567",
            "sms_code": "999999"
        }
        
        response = client.post("/api/v1/auth/signup", json=signup_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "קוד SMS שגוי" in response.json()["detail"]


class TestLogin:
    """Test user login"""
    
    def test_login_success(self, client, db_session):
        """Test successful login"""
        # Create user
        user = User(
            email="user@test.com",
            hashed_password=get_password_hash("password123"),
            full_name="Test User",
            id_number="123456789",
            phone_number="+972501234567",
            is_phone_verified=True,
            subscription_plan=SubscriptionPlan.FREE,
            receipt_limit=50
        )
        db_session.add(user)
        db_session.commit()
        
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "user@test.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        
        # Verify last_login updated
        db_session.refresh(user)
        assert user.last_login is not None
    
    def test_login_wrong_password(self, client, db_session):
        """Test login with wrong password"""
        user = User(
            email="user@test.com",
            hashed_password=get_password_hash("password123"),
            full_name="Test User",
            id_number="123456789",
            phone_number="+972501234567",
            is_phone_verified=True,
            subscription_plan=SubscriptionPlan.FREE,
            receipt_limit=50
        )
        db_session.add(user)
        db_session.commit()
        
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "user@test.com",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "שגויים" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent email"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@test.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_inactive_account(self, client, db_session):
        """Test login with inactive account"""
        user = User(
            email="inactive@test.com",
            hashed_password=get_password_hash("password123"),
            full_name="Inactive User",
            id_number="123456789",
            phone_number="+972501234567",
            is_phone_verified=True,
            is_active=False,
            subscription_plan=SubscriptionPlan.FREE,
            receipt_limit=50
        )
        db_session.add(user)
        db_session.commit()
        
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "inactive@test.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "לא פעיל" in response.json()["detail"]


class TestRefreshToken:
    """Test token refresh"""
    
    def test_refresh_token_success(self, client, db_session):
        """Test successful token refresh"""
        # Create user
        user = User(
            email="user@test.com",
            hashed_password=get_password_hash("password123"),
            full_name="Test User",
            id_number="123456789",
            phone_number="+972501234567",
            is_phone_verified=True,
            subscription_plan=SubscriptionPlan.FREE,
            receipt_limit=50
        )
        db_session.add(user)
        db_session.commit()
        
        # Generate refresh token
        from app.core.security import create_refresh_token
        refresh_token = create_refresh_token(data={"sub": user.id})
        
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
    
    def test_refresh_token_invalid(self, client):
        """Test refresh with invalid token"""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetCurrentUser:
    """Test get current user endpoint"""
    
    def test_get_current_user_success(self, client, db_session, auth_headers):
        """Test getting current user info"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "email" in data
        assert "full_name" in data
        assert "subscription_plan" in data
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting user info without authentication"""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestForgotPassword:
    """Test forgot password functionality"""
    
    @patch('app.services.email_service.email_service.send_password_reset_email')
    def test_forgot_password_success(self, mock_email, client, db_session):
        """Test forgot password request"""
        mock_email.return_value = True
        
        # Create user
        user = User(
            email="user@test.com",
            hashed_password=get_password_hash("password123"),
            full_name="Test User",
            id_number="123456789",
            phone_number="+972501234567",
            is_phone_verified=True,
            subscription_plan=SubscriptionPlan.FREE,
            receipt_limit=50
        )
        db_session.add(user)
        db_session.commit()
        
        response = client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "user@test.com"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "קישור לאיפוס סיסמה" in response.json()["message"]
    
    def test_forgot_password_nonexistent_email(self, client):
        """Test forgot password with nonexistent email (should still return success)"""
        response = client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "nonexistent@test.com"}
        )
        
        # Should return success to prevent email enumeration
        assert response.status_code == status.HTTP_200_OK


class TestResetPassword:
    """Test password reset"""
    
    def test_reset_password_success(self, client, db_session):
        """Test successful password reset"""
        # Create user
        user = User(
            email="user@test.com",
            hashed_password=get_password_hash("oldpassword"),
            full_name="Test User",
            id_number="123456789",
            phone_number="+972501234567",
            is_phone_verified=True,
            subscription_plan=SubscriptionPlan.FREE,
            receipt_limit=50
        )
        db_session.add(user)
        db_session.commit()
        
        # Generate reset token
        reset_token = create_access_token(
            data={"sub": user.id, "type": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        
        response = client.post(
            "/api/v1/auth/reset-password",
            json={
                "token": reset_token,
                "new_password": "NewSecure123!"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "שונתה בהצלחה" in response.json()["message"]
        
        # Verify password changed
        db_session.refresh(user)
        from app.core.security import verify_password
        assert verify_password("NewSecure123!", user.hashed_password)
    
    def test_reset_password_invalid_token(self, client):
        """Test password reset with invalid token"""
        response = client.post(
            "/api/v1/auth/reset-password",
            json={
                "token": "invalid_token",
                "new_password": "NewSecure123!"
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestChangePassword:
    """Test password change for authenticated users"""
    
    def test_change_password_success(self, client, db_session, auth_headers, test_user):
        """Test successful password change"""
        response = client.put(
            "/api/v1/auth/change-password",
            headers=auth_headers,
            json={
                "current_password": "password123",
                "new_password": "NewSecure123!"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "שונתה בהצלחה" in response.json()["message"]
        
        # Verify password changed
        db_session.refresh(test_user)
        from app.core.security import verify_password
        assert verify_password("NewSecure123!", test_user.hashed_password)
    
    def test_change_password_wrong_current(self, client, auth_headers):
        """Test password change with wrong current password"""
        response = client.put(
            "/api/v1/auth/change-password",
            headers=auth_headers,
            json={
                "current_password": "wrongpassword",
                "new_password": "NewSecure123!"
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "הנוכחית שגויה" in response.json()["detail"]
    
    def test_change_password_unauthorized(self, client):
        """Test password change without authentication"""
        response = client.put(
            "/api/v1/auth/change-password",
            json={
                "current_password": "password123",
                "new_password": "NewSecure123!"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestLogout:
    """Test logout endpoint"""
    
    def test_logout_success(self, client, auth_headers):
        """Test successful logout"""
        response = client.post("/api/v1/auth/logout", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert "התנתקת בהצלחה" in response.json()["message"]
    
    def test_logout_unauthorized(self, client):
        """Test logout without authentication"""
        response = client.post("/api/v1/auth/logout")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
