"""
Text Utilities
Hebrew text normalization and similarity functions
"""

import re
import unicodedata
from typing import Optional


def normalize_hebrew_text(text: str) -> str:
    """
    Normalize Hebrew text for comparison
    - Removes diacritics (nikud)
    - Normalizes whitespace
    - Converts to lowercase
    - Removes special characters
    
    Args:
        text: Hebrew text to normalize
    
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Remove Hebrew diacritics (nikud) - Unicode range U+0591 to U+05C7
    text = re.sub(r'[\u0591-\u05C7]', '', text)
    
    # Normalize Unicode (NFD = Canonical Decomposition)
    text = unicodedata.normalize('NFD', text)
    
    # Remove combining characters
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    # Remove special characters, keep only letters, numbers, and spaces
    text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
    
    # Convert to lowercase
    text = text.lower()
    
    return text


def clean_business_number(business_number: str) -> str:
    """
    Clean and normalize business number
    - Removes non-digit characters
    - Pads with leading zeros to 9 digits
    
    Args:
        business_number: Business number to clean
    
    Returns:
        Cleaned business number (9 digits)
    """
    if not business_number:
        return ""
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', business_number)
    
    # Pad with leading zeros to 9 digits
    return digits_only.zfill(9) if digits_only else ""


def extract_numbers_from_text(text: str) -> list:
    """
    Extract all numbers from text
    
    Args:
        text: Text to extract numbers from
    
    Returns:
        List of numbers as strings
    """
    if not text:
        return []
    
    return re.findall(r'\d+', text)


def is_hebrew(text: str) -> bool:
    """
    Check if text contains Hebrew characters
    
    Args:
        text: Text to check
    
    Returns:
        True if text contains Hebrew
    """
    if not text:
        return False
    
    # Hebrew Unicode range: U+0590 to U+05FF
    return bool(re.search(r'[\u0590-\u05FF]', text))


def truncate_with_ellipsis(text: str, max_length: int = 50) -> str:
    """
    Truncate text and add ellipsis if needed
    
    Args:
        text: Text to truncate
        max_length: Maximum length
    
    Returns:
        Truncated text with ellipsis
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage
    - Removes path separators
    - Removes special characters
    - Limits length
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    if not filename:
        return "unnamed"
    
    # Remove path separators
    filename = filename.replace('/', '_').replace('\\', '_')
    
    # Remove special characters except dot, dash, underscore
    filename = re.sub(r'[^\w\-\.]', '_', filename)
    
    # Limit length
    name_parts = filename.rsplit('.', 1)
    if len(name_parts) == 2:
        name, ext = name_parts
        if len(name) > 50:
            name = name[:50]
        filename = f"{name}.{ext}"
    else:
        filename = filename[:50]
    
    return filename


def highlight_search_term(text: str, search_term: str, max_length: int = 100) -> str:
    """
    Extract snippet of text around search term
    
    Args:
        text: Full text
        search_term: Term to find
        max_length: Maximum snippet length
    
    Returns:
        Snippet with search term highlighted
    """
    if not text or not search_term:
        return truncate_with_ellipsis(text, max_length)
    
    # Find position of search term (case-insensitive)
    pos = text.lower().find(search_term.lower())
    
    if pos == -1:
        return truncate_with_ellipsis(text, max_length)
    
    # Calculate snippet boundaries
    half_length = max_length // 2
    start = max(0, pos - half_length)
    end = min(len(text), pos + len(search_term) + half_length)
    
    snippet = text[start:end]
    
    # Add ellipsis
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    
    return snippet
