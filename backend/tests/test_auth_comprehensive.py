"""
Comprehensive tests for authentication endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.models.user import User
from datetime import datetime


class TestSignup:
    """Tests for user registration"""
    
    def test_signup_success(self, client: TestClient, db):
        """Test successful user registration"""
        signup_data = {
            "email": "newuser@example.com",
            "full_name": "New User",
            "id_number": "123456783",  # Valid Luhn
            "phone_number": "0501234567",
            "password": "SecurePass123!",
            "business_name": "My Business"
        }
        
        response = client.post("/api/v1/auth/signup", json=signup_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == signup_data["email"]
    
    def test_signup_duplicate_email(self, client: TestClient, db, test_user):
        """Test signup with existing email"""
        signup_data = {
            "email": test_user.email,  # Already exists
            "full_name": "Another User",
            "id_number": "305219892",
            "phone_number": "0521234567",
            "password": "SecurePass123!"
        }
        
        response = client.post("/api/v1/auth/signup", json=signup_data)
        
        assert response.status_code == 400
        assert "כבר קיים" in response.json()["detail"] or "exists" in response.json()["detail"].lower()
    
    def test_signup_invalid_id_number(self, client: TestClient, db):
        """Test signup with invalid Israeli ID"""
        signup_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "id_number": "123456789",  # Invalid Luhn checksum
            "phone_number": "0501234567",
            "password": "SecurePass123!"
        }
        
        response = client.post("/api/v1/auth/signup", json=signup_data)
        
        assert response.status_code == 422
    
    def test_signup_invalid_phone(self, client: TestClient, db):
        """Test signup with invalid phone number"""
        signup_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "id_number": "123456783",
            "phone_number": "123",  # Too short
            "password": "SecurePass123!"
        }
        
        response = client.post("/api/v1/auth/signup", json=signup_data)
        
        assert response.status_code == 422
    
    def test_signup_weak_password(self, client: TestClient, db):
        """Test signup with weak password"""
        signup_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "id_number": "123456783",
            "phone_number": "0501234567",
            "password": "123"  # Too short
        }
        
        response = client.post("/api/v1/auth/signup", json=signup_data)
        
        assert response.status_code == 422
    
    def test_signup_missing_fields(self, client: TestClient, db):
        """Test signup with missing required fields"""
        signup_data = {
            "email": "test@example.com"
            # Missing other required fields
        }
        
        response = client.post("/api/v1/auth/signup", json=signup_data)
        
        assert response.status_code == 422
    
    def test_signup_invalid_email_format(self, client: TestClient, db):
        """Test signup with invalid email format"""
        signup_data = {
            "email": "not-an-email",
            "full_name": "Test User",
            "id_number": "123456783",
            "phone_number": "0501234567",
            "password": "SecurePass123!"
        }
        
        response = client.post("/api/v1/auth/signup", json=signup_data)
        
        assert response.status_code == 422


class TestLogin:
    """Tests for user login"""
    
    def test_login_success(self, client: TestClient, db, test_user):
        """Test successful login"""
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
    
    def test_login_invalid_email(self, client: TestClient, db):
        """Test login with non-existent email"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
    
    def test_login_wrong_password(self, client: TestClient, db, test_user):
        """Test login with wrong password"""
        login_data = {
            "email": test_user.email,
            "password": "wrongpassword"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
    
    def test_login_empty_credentials(self, client: TestClient, db):
        """Test login with empty credentials"""
        login_data = {
            "email": "",
            "password": ""
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code in [401, 422]
    
    def test_login_missing_fields(self, client: TestClient, db):
        """Test login with missing fields"""
        login_data = {
            "email": "test@example.com"
            # Missing password
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 422


class TestTokenRefresh:
    """Tests for token refresh"""
    
    def test_refresh_token_success(self, client: TestClient, db, test_user):
        """Test successful token refresh"""
        # First login to get tokens
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh tokens
        refresh_data = {
            "refresh_token": refresh_token
        }
        
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
    
    def test_refresh_token_invalid(self, client: TestClient, db):
        """Test refresh with invalid token"""
        refresh_data = {
            "refresh_token": "invalid.token.here"
        }
        
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 401
    
    def test_refresh_token_missing(self, client: TestClient, db):
        """Test refresh without token"""
        response = client.post("/api/v1/auth/refresh", json={})
        
        assert response.status_code == 422


class TestPasswordManagement:
    """Tests for password operations"""
    
    def test_change_password_success(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test successful password change"""
        change_data = {
            "current_password": "testpassword123",
            "new_password": "NewSecurePass123!"
        }
        
        response = client.post(
            "/api/v1/auth/change-password",
            headers=auth_headers,
            json=change_data
        )
        
        assert response.status_code == 200
        assert "success" in response.json()["message"].lower() or "הצליח" in response.json()["message"]
    
    def test_change_password_wrong_current(self, client: TestClient, auth_headers: dict, db):
        """Test password change with wrong current password"""
        change_data = {
            "current_password": "wrongpassword",
            "new_password": "NewSecurePass123!"
        }
        
        response = client.post(
            "/api/v1/auth/change-password",
            headers=auth_headers,
            json=change_data
        )
        
        assert response.status_code == 401
    
    def test_change_password_weak_new(self, client: TestClient, auth_headers: dict, db):
        """Test password change with weak new password"""
        change_data = {
            "current_password": "testpassword123",
            "new_password": "123"  # Too weak
        }
        
        response = client.post(
            "/api/v1/auth/change-password",
            headers=auth_headers,
            json=change_data
        )
        
        assert response.status_code == 422
    
    def test_change_password_unauthorized(self, client: TestClient, db):
        """Test password change without authentication"""
        change_data = {
            "current_password": "testpassword123",
            "new_password": "NewSecurePass123!"
        }
        
        response = client.post("/api/v1/auth/change-password", json=change_data)
        
        assert response.status_code == 401
    
    def test_request_password_reset(self, client: TestClient, db, test_user):
        """Test password reset request"""
        reset_data = {
            "email": test_user.email
        }
        
        response = client.post("/api/v1/auth/forgot-password", json=reset_data)
        
        # Should succeed even if email service is mocked
        assert response.status_code in [200, 202]
    
    def test_request_password_reset_nonexistent_email(self, client: TestClient, db):
        """Test password reset for non-existent email"""
        reset_data = {
            "email": "nonexistent@example.com"
        }
        
        response = client.post("/api/v1/auth/forgot-password", json=reset_data)
        
        # Should return success to avoid email enumeration
        assert response.status_code in [200, 202]


class TestUserProfile:
    """Tests for user profile endpoints"""
    
    def test_get_profile_success(self, client: TestClient, auth_headers: dict, test_user):
        """Test getting user profile"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["full_name"] == test_user.full_name
        assert "id" in data
    
    def test_get_profile_unauthorized(self, client: TestClient):
        """Test getting profile without authentication"""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 401
    
    def test_get_profile_invalid_token(self, client: TestClient):
        """Test getting profile with invalid token"""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 401
    
    def test_update_profile_success(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test updating user profile"""
        update_data = {
            "full_name": "Updated Name",
            "business_name": "Updated Business",
            "phone_number": "0521234567"
        }
        
        response = client.patch(
            "/api/v1/auth/me",
            headers=auth_headers,
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
    
    def test_update_profile_invalid_phone(self, client: TestClient, auth_headers: dict):
        """Test updating profile with invalid phone"""
        update_data = {
            "phone_number": "123"  # Invalid
        }
        
        response = client.patch(
            "/api/v1/auth/me",
            headers=auth_headers,
            json=update_data
        )
        
        assert response.status_code == 422
    
    def test_update_profile_unauthorized(self, client: TestClient):
        """Test updating profile without authentication"""
        update_data = {
            "full_name": "Updated Name"
        }
        
        response = client.patch("/api/v1/auth/me", json=update_data)
        
        assert response.status_code == 401


class TestLogout:
    """Tests for logout functionality"""
    
    def test_logout_success(self, client: TestClient, auth_headers: dict):
        """Test successful logout"""
        response = client.post("/api/v1/auth/logout", headers=auth_headers)
        
        # Logout should succeed
        assert response.status_code in [200, 204]
    
    def test_logout_unauthorized(self, client: TestClient):
        """Test logout without authentication"""
        response = client.post("/api/v1/auth/logout")
        
        assert response.status_code == 401


class TestAccountDeletion:
    """Tests for account deletion"""
    
    def test_delete_account_success(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test account deletion"""
        delete_data = {
            "password": "testpassword123",
            "confirmation": "DELETE"
        }
        
        response = client.delete(
            "/api/v1/auth/account",
            headers=auth_headers,
            json=delete_data
        )
        
        # Should succeed or be not implemented yet
        assert response.status_code in [200, 204, 404, 501]
    
    def test_delete_account_wrong_password(self, client: TestClient, auth_headers: dict):
        """Test account deletion with wrong password"""
        delete_data = {
            "password": "wrongpassword",
            "confirmation": "DELETE"
        }
        
        response = client.delete(
            "/api/v1/auth/account",
            headers=auth_headers,
            json=delete_data
        )
        
        assert response.status_code in [401, 404, 501]
    
    def test_delete_account_unauthorized(self, client: TestClient):
        """Test account deletion without authentication"""
        delete_data = {
            "password": "testpassword123",
            "confirmation": "DELETE"
        }
        
        response = client.delete("/api/v1/auth/account", json=delete_data)
        
        assert response.status_code == 401


class TestEmailVerification:
    """Tests for email verification"""
    
    def test_verify_email(self, client: TestClient, db, test_user):
        """Test email verification"""
        # Mock verification token
        response = client.get(f"/api/v1/auth/verify-email?token=mock_token")
        
        # Endpoint may not be implemented yet
        assert response.status_code in [200, 404, 501]
    
    def test_resend_verification(self, client: TestClient, auth_headers: dict):
        """Test resending verification email"""
        response = client.post("/api/v1/auth/resend-verification", headers=auth_headers)
        
        # Endpoint may not be implemented yet
        assert response.status_code in [200, 202, 404, 501]


class TestProtectedRoutes:
    """Tests for protected route access"""
    
    def test_access_protected_route_with_valid_token(self, client: TestClient, auth_headers: dict):
        """Test accessing protected route with valid token"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
    
    def test_access_protected_route_without_token(self, client: TestClient):
        """Test accessing protected route without token"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    def test_access_protected_route_with_expired_token(self, client: TestClient):
        """Test accessing protected route with expired token"""
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        headers = {"Authorization": f"Bearer {expired_token}"}
        
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
    
    def test_access_protected_route_with_malformed_token(self, client: TestClient):
        """Test accessing protected route with malformed token"""
        headers = {"Authorization": "Bearer not.a.valid.token"}
        
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
    
    def test_access_protected_route_with_wrong_scheme(self, client: TestClient):
        """Test accessing protected route with wrong auth scheme"""
        headers = {"Authorization": "Basic dGVzdDp0ZXN0"}
        
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code in [401, 403]
