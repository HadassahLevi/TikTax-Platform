"""
Manual Test Script for Error Handling and Logging
Demonstrates the error handling infrastructure in action

Run with: python test_error_handling_manual.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.logging_config import setup_logging, get_logger
from app.core.exceptions import (
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
    DatabaseError
)

# Setup logging
setup_logging()
logger = get_logger(__name__)


def test_logging():
    """Test structured JSON logging"""
    print("\n" + "="*60)
    print("TESTING STRUCTURED LOGGING")
    print("="*60 + "\n")
    
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Log with extra context
    logger.info(
        "User logged in successfully",
        extra={
            "user_id": 123,
            "request_id": "abc-123-def",
            "ip_address": "192.168.1.1"
        }
    )
    
    print("✅ Logging test complete - check logs/app.log for JSON output\n")


def test_exceptions():
    """Test all custom exceptions"""
    print("\n" + "="*60)
    print("TESTING CUSTOM EXCEPTIONS")
    print("="*60 + "\n")
    
    exceptions_to_test = [
        ("AuthenticationError", AuthenticationError()),
        ("AuthorizationError", AuthorizationError()),
        ("ResourceNotFoundError", ResourceNotFoundError(resource="Receipt", resource_he="קבלה")),
        ("ValidationError", ValidationError("Invalid email", "אימייל לא תקין", {"field": "email"})),
        ("DuplicateResourceError", DuplicateResourceError(resource="User", resource_he="משתמש")),
        ("ExternalServiceError", ExternalServiceError("OCR", "API timeout", "תם הזמן")),
        ("RateLimitError", RateLimitError()),
        ("SubscriptionLimitError", SubscriptionLimitError(limit=100)),
        ("FileUploadError", FileUploadError("File too large", "קובץ גדול מדי")),
        ("OCRProcessingError", OCRProcessingError()),
        ("DatabaseError", DatabaseError("insert", "Connection timeout"))
    ]
    
    for name, exc in exceptions_to_test:
        print(f"\n{name}:")
        print(f"  Status Code: {exc.status_code}")
        print(f"  Message (EN): {exc.message}")
        print(f"  Message (HE): {exc.message_he}")
        print(f"  Details: {exc.details}")
        print(f"  ✅ Has Hebrew: {'✓' if any('\\u0590' <= c <= '\\u05FF' for c in exc.message_he) else '✗'}")
    
    print("\n✅ All exceptions tested successfully\n")


def test_error_response_format():
    """Test error response format"""
    print("\n" + "="*60)
    print("TESTING ERROR RESPONSE FORMAT")
    print("="*60 + "\n")
    
    exc = ValidationError(
        message="Invalid input",
        message_he="קלט לא תקין",
        details={"field": "email", "reason": "Invalid format"}
    )
    
    print("Exception response detail:")
    print(f"  {exc.detail}\n")
    
    # Verify structure
    assert "error" in exc.detail, "Missing 'error' field"
    assert "error_he" in exc.detail, "Missing 'error_he' field"
    assert "details" in exc.detail, "Missing 'details' field"
    
    print("✅ Response format is correct\n")


def test_sensitive_data_filtering():
    """Test that sensitive data is filtered from logs"""
    print("\n" + "="*60)
    print("TESTING SENSITIVE DATA FILTERING")
    print("="*60 + "\n")
    
    # Try to log sensitive data
    logger.info("User password is secret123")  # Should be filtered
    logger.info("API token: abc-123-def")  # Should be filtered
    logger.info("User logged in successfully")  # Should NOT be filtered
    
    print("✅ Sensitive data filtering test complete")
    print("   Check logs/app.log - sensitive patterns should be [FILTERED]\n")


def test_exception_with_logging():
    """Test exception handling with logging"""
    print("\n" + "="*60)
    print("TESTING EXCEPTION + LOGGING")
    print("="*60 + "\n")
    
    try:
        logger.info("Attempting database operation...")
        raise DatabaseError("insert", "Connection timeout")
    except DatabaseError as e:
        logger.error(
            f"Database operation failed: {e.message}",
            extra={
                "user_id": 456,
                "request_id": "xyz-789",
                "operation": e.details.get("operation")
            },
            exc_info=True
        )
        print(f"✅ Exception logged: {e.message}")
        print(f"   Status: {e.status_code}")
        print(f"   Hebrew: {e.message_he}\n")


def main():
    """Run all manual tests"""
    print("\n" + "="*60)
    print("TIK-TAX ERROR HANDLING MANUAL TESTS")
    print("="*60)
    
    try:
        test_logging()
        test_exceptions()
        test_error_response_format()
        test_sensitive_data_filtering()
        test_exception_with_logging()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY! ✅")
        print("="*60)
        print("\nNext steps:")
        print("1. Check logs/app.log for JSON-formatted logs")
        print("2. Check logs/errors.log for error-only logs")
        print("3. Run pytest: python -m pytest tests/test_error_handling.py -v")
        print("4. Test Sentry integration (requires SENTRY_DSN in .env)")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
