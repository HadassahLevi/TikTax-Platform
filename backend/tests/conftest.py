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

# Test database URL
SQLALCHEMY_DATABASE_URL = "postgresql://tiktax:password@localhost:5432/tiktax_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
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
    from app.models.user import User
    from app.core.security import get_password_hash
    
    user = User(
        id="test-user-id",
        email="test@example.com",
        password_hash=get_password_hash("TestPassword123"),
        phone="+972501234567",
        first_name="Test",
        last_name="User",
        is_active=True,
        is_verified=True
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
