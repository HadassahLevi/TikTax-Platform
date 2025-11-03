"""
General Helper Utilities
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional


def generate_id() -> str:
    """
    Generate unique ID
    
    Returns:
        UUID string
    """
    return str(uuid.uuid4())


def get_current_timestamp() -> datetime:
    """
    Get current UTC timestamp
    
    Returns:
        Current datetime
    """
    return datetime.utcnow()


def add_days(date: datetime, days: int) -> datetime:
    """
    Add days to date
    
    Args:
        date: Starting date
        days: Number of days to add
        
    Returns:
        New datetime
    """
    return date + timedelta(days=days)


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate string to max length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def parse_date_string(date_string: str, format: str = "%Y-%m-%d") -> Optional[datetime]:
    """
    Parse date string to datetime
    
    Args:
        date_string: Date string
        format: Date format
        
    Returns:
        Datetime object or None if invalid
    """
    try:
        return datetime.strptime(date_string, format)
    except ValueError:
        return None
