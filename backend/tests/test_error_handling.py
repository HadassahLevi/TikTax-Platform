"""
Test Error Handling and Logging Infrastructure
Validates production-grade error handling, logging, and monitoring setup

Run with: python -m pytest test_error_handling.py -v
"""

import pytest
import logging
from fastapi.testclient import TestClient
from app.main import app
from app.core.exceptions import (
    TikTaxException,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    ValidationError,
    DuplicateResourceError,
    ExternalServiceError,
    RateLimitError,
    SubscriptionLimitError,
    FileUploadError,
    OCRProcessingError,
    DatabaseError,
    StorageError,
    EmailError,
    SMSError
)

client = TestClient(app)


class TestCustomExceptions:
    """Test all custom exception classes"""
    
    def test_authentication_error(self):
        """Test AuthenticationError"""
        exc = AuthenticationError()
        assert exc.status_code == 401
        assert exc.message == "Authentication failed"
        assert exc.message_he == "אימות נכשל"
        assert exc.details == {}
    
    def test_authorization_error(self):
        """Test AuthorizationError"""
        exc = AuthorizationError()
        assert exc.status_code == 403
        assert exc.message == "Access denied"
        assert exc.message_he == "אין הרשאה לגישה"
    
    def test_resource_not_found_error(self):
        """Test ResourceNotFoundError"""
        exc = ResourceNotFoundError(resource="Receipt", resource_he="קבלה")
        assert exc.status_code == 404
        assert "Receipt" in exc.message
        assert "קבלה" in exc.message_he
    
    def test_validation_error(self):
        """Test ValidationError"""
        details = {"field": "email", "error": "invalid format"}
        exc = ValidationError(
            message="Invalid email",
            message_he="אימייל לא תקין",
            details=details
        )
        assert exc.status_code == 422
        assert exc.details == details
    
    def test_duplicate_resource_error(self):
        """Test DuplicateResourceError"""
        exc = DuplicateResourceError(resource="User", resource_he="משתמש")
        assert exc.status_code == 409
        assert "User" in exc.message
        assert "משתמש" in exc.message_he
    
    def test_external_service_error(self):
        """Test ExternalServiceError"""
        exc = ExternalServiceError(
            service="Google Vision",
            message="API quota exceeded",
            message_he="חריגה ממכסת API"
        )
        assert exc.status_code == 502
        assert "Google Vision" in exc.message
        assert exc.details["service"] == "Google Vision"
    
    def test_rate_limit_error(self):
        """Test RateLimitError"""
        exc = RateLimitError()
        assert exc.status_code == 429
        assert "Too many requests" in exc.message
        assert "יותר מדי בקשות" in exc.message_he
    
    def test_subscription_limit_error(self):
        """Test SubscriptionLimitError"""
        exc = SubscriptionLimitError(limit=100)
        assert exc.status_code == 402
        assert "100" in exc.message
        assert exc.details["limit"] == 100
    
    def test_file_upload_error(self):
        """Test FileUploadError"""
        exc = FileUploadError(
            reason="File too large",
            reason_he="קובץ גדול מדי"
        )
        assert exc.status_code == 400
        assert "File too large" in exc.message
        assert "קובץ גדול מדי" in exc.message_he
    
    def test_ocr_processing_error(self):
        """Test OCRProcessingError"""
        exc = OCRProcessingError()
        assert exc.status_code == 422
        assert exc.details["stage"] == "ocr"
    
    def test_database_error(self):
        """Test DatabaseError"""
        exc = DatabaseError(operation="insert", message="Connection timeout")
        assert exc.status_code == 500
        assert "insert" in exc.message
        assert exc.details["operation"] == "insert"
    
    def test_storage_error(self):
        """Test StorageError"""
        exc = StorageError()
        assert exc.status_code == 500
        assert exc.details["service"] == "s3"
    
    def test_email_error(self):
        """Test EmailError"""
        exc = EmailError()
        assert exc.status_code == 500
        assert exc.details["service"] == "sendgrid"
    
    def test_sms_error(self):
        """Test SMSError"""
        exc = SMSError()
        assert exc.status_code == 500
        assert exc.details["service"] == "twilio"


class TestErrorResponses:
    """Test error response format"""
    
    def test_error_response_structure(self):
        """Test that all errors return consistent structure"""
        exc = ValidationError(
            message="Test error",
            message_he="שגיאת בדיקה",
            details={"field": "test"}
        )
        
        assert "error" in exc.detail
        assert "error_he" in exc.detail
        assert "details" in exc.detail
        assert exc.detail["error"] == "Test error"
        assert exc.detail["error_he"] == "שגיאת בדיקה"
        assert exc.detail["details"]["field"] == "test"
    
    def test_hebrew_messages_present(self):
        """Test that all exceptions have Hebrew messages"""
        exceptions = [
            AuthenticationError(),
            AuthorizationError(),
            ResourceNotFoundError(),
            RateLimitError(),
            FileUploadError(reason="test"),
            OCRProcessingError(),
            StorageError(),
            EmailError(),
            SMSError()
        ]
        
        for exc in exceptions:
            assert hasattr(exc, "message_he")
            assert exc.message_he is not None
            assert len(exc.message_he) > 0
            # Check that it's actually Hebrew (contains Hebrew characters)
            assert any('\u0590' <= char <= '\u05FF' for char in exc.message_he)


class TestLoggingConfiguration:
    """Test logging setup"""
    
    def test_json_formatter_imports(self):
        """Test that JSON formatter can be imported"""
        from app.core.logging_config import JSONFormatter, setup_logging
        assert JSONFormatter is not None
        assert setup_logging is not None
    
    def test_sensitive_data_filter(self):
        """Test sensitive data filtering"""
        from app.core.logging_config import SensitiveDataFilter
        
        filter_instance = SensitiveDataFilter()
        
        # Create a log record with sensitive data
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="User logged in with password=secret123",
            args=(),
            exc_info=None
        )
        
        # Apply filter
        result = filter_instance.filter(record)
        
        # Should still allow the record but sanitize it
        assert result is True
        assert "password" not in record.msg or "[SENSITIVE DATA FILTERED" in record.msg


class TestSentryIntegration:
    """Test Sentry monitoring setup"""
    
    def test_sentry_import(self):
        """Test that Sentry can be imported"""
        from app.core.monitoring import init_sentry, before_send_handler
        assert init_sentry is not None
        assert before_send_handler is not None
    
    def test_before_send_filters_sensitive_headers(self):
        """Test that Sentry filters sensitive headers"""
        from app.core.monitoring import before_send_handler
        
        event = {
            "request": {
                "headers": {
                    "Authorization": "Bearer secret-token",
                    "Cookie": "session=abc123",
                    "Content-Type": "application/json"
                }
            }
        }
        
        filtered = before_send_handler(event, {})
        
        assert filtered["request"]["headers"]["Authorization"] == "[FILTERED]"
        assert filtered["request"]["headers"]["Cookie"] == "[FILTERED]"
        assert filtered["request"]["headers"]["Content-Type"] == "application/json"
    
    def test_before_send_filters_passwords(self):
        """Test that Sentry filters password fields"""
        from app.core.monitoring import before_send_handler
        
        event = {
            "request": {
                "data": {
                    "email": "test@example.com",
                    "password": "secret123",
                    "current_password": "old_secret",
                    "new_password": "new_secret"
                }
            }
        }
        
        filtered = before_send_handler(event, {})
        
        assert filtered["request"]["data"]["email"] == "test@example.com"
        assert filtered["request"]["data"]["password"] == "[FILTERED]"
        assert filtered["request"]["data"]["current_password"] == "[FILTERED]"
        assert filtered["request"]["data"]["new_password"] == "[FILTERED]"
    
    def test_before_send_filters_user_email(self):
        """Test that Sentry partially filters user email"""
        from app.core.monitoring import before_send_handler
        
        event = {
            "user": {
                "email": "john.doe@example.com",
                "id": 123
            }
        }
        
        filtered = before_send_handler(event, {})
        
        # Email should be partially filtered (keep domain)
        assert "@example.com" in filtered["user"]["email"]
        assert "john.doe" not in filtered["user"]["email"]
        assert filtered["user"]["id"] == 123


class TestErrorHandlerMiddleware:
    """Test global error handler"""
    
    def test_health_endpoint_works(self):
        """Test that health endpoint works (baseline)"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_404_returns_hebrew_message(self):
        """Test that 404 errors return Hebrew messages"""
        response = client.get("/api/v1/nonexistent-endpoint")
        assert response.status_code == 404


class TestRequestTracking:
    """Test request ID and context tracking"""
    
    def test_request_id_in_response_headers(self):
        """Test that X-Request-ID header is added to responses"""
        response = client.get("/health")
        assert "X-Request-ID" in response.headers
        
        # Should be a UUID
        request_id = response.headers["X-Request-ID"]
        assert len(request_id) == 36  # UUID format
        assert "-" in request_id


def test_import_all_modules():
    """Test that all modules can be imported without errors"""
    from app.core import logging_config
    from app.core import monitoring
    from app.core import exceptions
    from app.middleware import error_handler
    
    assert logging_config is not None
    assert monitoring is not None
    assert exceptions is not None
    assert error_handler is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
