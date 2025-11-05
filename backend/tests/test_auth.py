import pytest
from fastapi import status

def test_signup_success(client, db):
    """Test successful user signup"""
    response = client.post("/api/v1/auth/signup", json={
        "email": "newuser@example.com",
        "password": "Strong123!@#",
        "full_name": "New User",
        "id_number": "987654321",
        "phone": "+972501234567",
        "business_name": "New Business",
        "business_number": "520123456"
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "access_token" in data
    assert "refresh_token" in data


def test_signup_duplicate_email(client, test_user):
    """Test signup with existing email"""
    response = client.post("/api/v1/auth/signup", json={
        "email": test_user.email,
        "password": "Strong123!@#",
        "full_name": "Duplicate User",
        "id_number": "111111111",
        "phone": "+972509999999",
        "business_name": "Duplicate Business",
        "business_number": "530111111"
    })
    
    assert response.status_code == status.HTTP_409_CONFLICT


def test_signup_weak_password(client):
    """Test signup with weak password"""
    response = client.post("/api/v1/auth/signup", json={
        "email": "weak@example.com",
        "password": "123",
        "full_name": "Weak Password User",
        "id_number": "222222222",
        "phone": "+972508888888",
        "business_name": "Weak Business",
        "business_number": "540222222"
    })
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_signup_invalid_israeli_id(client):
    """Test signup with invalid Israeli ID"""
    response = client.post("/api/v1/auth/signup", json={
        "email": "invalid@example.com",
        "password": "Strong123!@#",
        "full_name": "Invalid ID User",
        "id_number": "000000000",
        "phone": "+972507777777",
        "business_name": "Invalid Business",
        "business_number": "550333333"
    })
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "Test123!@#"
    })
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == test_user.email


def test_login_wrong_password(client, test_user):
    """Test login with wrong password"""
    response = client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "WrongPassword123"
    })
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    response = client.post("/api/v1/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "AnyPassword123"
    })
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, auth_headers, test_user):
    """Test getting current user"""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user.email
    assert data["full_name"] == test_user.full_name


def test_get_current_user_no_auth(client):
    """Test getting current user without authentication"""
    response = client.get("/api/v1/auth/me")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token(client, test_user):
    """Test token refresh"""
    # Login first
    login_response = client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "Test123!@#"
    })
    refresh_token = login_response.json()["refresh_token"]
    
    # Refresh token
    response = client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data


def test_change_password(client, auth_headers, test_user):
    """Test password change"""
    response = client.put("/api/v1/auth/change-password", 
        headers=auth_headers,
        json={
            "current_password": "Test123!@#",
            "new_password": "NewPassword123!@#"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    # Verify old password doesn't work
    login_old = client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "Test123!@#"
    })
    assert login_old.status_code == status.HTTP_401_UNAUTHORIZED
    
    # Verify new password works
    login_new = client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "NewPassword123!@#"
    })
    assert login_new.status_code == status.HTTP_200_OK
