import pytest
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set test environment variables BEFORE importing app
os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test-secret-key-for-jwt-tokens-1234567890"
os.environ["GOOGLE_CLOUD_VISION_CREDENTIALS"] = "test_credentials.json"
os.environ["AWS_ACCESS_KEY_ID"] = "test_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test_secret"
os.environ["S3_BUCKET_NAME"] = "test-bucket"

# Mock Google Vision Client before any imports
mock_vision_client = MagicMock()
mock_vision_client.text_detection.return_value.text_annotations = []

# Patch Google Vision before importing app
with patch('google.cloud.vision.ImageAnnotatorClient', return_value=mock_vision_client):
    with patch('google.oauth2.service_account.Credentials.from_service_account_file'):
        from app.main import app
        from app.db.base import Base
        from app.db.session import get_db
        from app.core.security import create_access_token
        from app.models.category import Category

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Create test database and session"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client with database"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    """Create test user"""
    from app.services.auth_service import AuthService
    
    user_data = {
        "email": "test@example.com",
        "password": "Test123!@#",
        "full_name": "Test User",
        "id_number": "123456789",
        "phone": "+972501234567",
        "business_name": "Test Business",
        "business_number": "510502466"
    }
    
    user = AuthService.create_user(db, **user_data)
    db.commit()
    return user


@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers"""
    token = create_access_token({"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_categories(db):
    """Create test categories"""
    categories = [
        Category(name_he="ציוד משרדי", name_en="Office Supplies", icon="briefcase", sort_order=1),
        Category(name_he="שירותים מקצועיים", name_en="Professional Services", icon="users", sort_order=2),
        Category(name_he="שיווק ופרסום", name_en="Marketing", icon="megaphone", sort_order=3)
    ]
    for cat in categories:
        db.add(cat)
    db.commit()
    return categories


@pytest.fixture
def test_receipt_data():
    """Sample receipt data for testing"""
    return {
        "vendor_name": "סופר-פארם",
        "business_number": "510502466",
        "date": "2025-10-26",
        "total_amount": 156.50,
        "vat_amount": 22.65,
        "pre_vat_amount": 133.85,
        "receipt_number": "12345678",
        "category_id": 1
    }
"""
Pytest configuration and fixtures
"""

import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.core.dependencies import get_db

# Test database URL - use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine"""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator:
    """Create test database session"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    """Create test client"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create test user"""
    from app.models.user import User, SubscriptionPlan
    from app.core.security import get_password_hash
    
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test User",
        id_number="123456789",
        phone_number="+972501234567",
        is_phone_verified=True,
        is_active=True,
        subscription_plan=SubscriptionPlan.FREE,
        receipt_limit=50,
        receipts_used_this_month=0
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user


@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers"""
    from app.core.security import create_access_token
    
    access_token = create_access_token(data={"sub": test_user.id})
    
    return {"Authorization": f"Bearer {access_token}"}
