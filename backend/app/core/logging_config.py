"""
Structured JSON Logging Configuration for Tik-Tax API
Provides production-grade logging with JSON formatting, request tracking, and sensitive data filtering
"""

import logging
import sys
from datetime import datetime
from typing import Any, Dict
import json
import os


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging
    
    Outputs logs in JSON format for easy parsing by log aggregation tools.
    Includes context fields like user_id, request_id, and IP address when available.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON
        
        Args:
            record: LogRecord instance containing log information
            
        Returns:
            JSON string with log data
        """
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            log_data["exc_type"] = record.exc_info[0].__name__ if record.exc_info[0] else None
        
        # Add extra context fields
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "ip_address"):
            log_data["ip_address"] = record.ip_address
        if hasattr(record, "method"):
            log_data["method"] = record.method
        if hasattr(record, "path"):
            log_data["path"] = record.path
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
            
        return json.dumps(log_data, ensure_ascii=False)


class SensitiveDataFilter(logging.Filter):
    """
    Filter to prevent logging of sensitive data
    
    Scans log messages for patterns that might contain sensitive information
    and replaces them with [FILTERED]
    """
    
    SENSITIVE_PATTERNS = [
        "password",
        "token",
        "secret",
        "api_key",
        "apikey",
        "authorization",
        "credit_card",
        "ssn",
        "social_security"
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter log record to remove sensitive data
        
        Args:
            record: LogRecord to filter
            
        Returns:
            True (always allow the record, but sanitize it first)
        """
        message = record.getMessage().lower()
        
        # Check if message contains sensitive patterns
        for pattern in self.SENSITIVE_PATTERNS:
            if pattern in message:
                # Don't log the actual message if it contains sensitive data
                record.msg = f"[SENSITIVE DATA FILTERED - contains '{pattern}']"
                record.args = ()
                
        return True


def setup_logging():
    """
    Configure application logging with JSON formatting and file rotation
    
    Sets up:
    - Console handler with JSON formatting for structured logs
    - File handler for errors with rotation (10MB max, 5 backups)
    - Sensitive data filtering
    - Suppression of noisy third-party library logs
    """
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove any existing handlers (avoid duplicate logs)
    root_logger.handlers = []
    
    # Console handler with JSON formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(JSONFormatter())
    console_handler.addFilter(SensitiveDataFilter())
    root_logger.addHandler(console_handler)
    
    # File handler for errors with rotation
    from logging.handlers import RotatingFileHandler
    
    error_log_path = os.path.join(logs_dir, "errors.log")
    error_handler = RotatingFileHandler(
        error_log_path,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    error_handler.addFilter(SensitiveDataFilter())
    root_logger.addHandler(error_handler)
    
    # File handler for all logs with rotation
    all_logs_path = os.path.join(logs_dir, "app.log")
    app_handler = RotatingFileHandler(
        all_logs_path,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(JSONFormatter())
    app_handler.addFilter(SensitiveDataFilter())
    root_logger.addHandler(app_handler)
    
    # Suppress noisy third-party library logs
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("s3transfer").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("google.cloud").setLevel(logging.WARNING)
    logging.getLogger("google.auth").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("Structured JSON logging initialized", extra={
        "logs_directory": logs_dir,
        "error_log": error_log_path,
        "app_log": all_logs_path
    })


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name
    
    Args:
        name: Name for the logger (typically __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
