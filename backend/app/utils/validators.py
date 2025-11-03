"""
Israeli Validators
Validation utilities for Israeli-specific data
"""

import re
from typing import Optional


def validate_israeli_id(id_number: str) -> bool:
    """
    Validate Israeli ID number using Luhn algorithm
    
    Args:
        id_number: ID number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Remove non-digits
    digits = ''.join(filter(str.isdigit, id_number))
    
    # Must be 9 digits
    if len(digits) != 9:
        return False
    
    # Luhn algorithm
    total = 0
    for i, digit in enumerate(digits):
        num = int(digit)
        if i % 2 == 0:
            num *= 2
            if num > 9:
                num = num // 10 + num % 10
        total += num
    
    return total % 10 == 0


def validate_israeli_phone(phone: str) -> bool:
    """
    Validate Israeli phone number
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Remove non-digits
    digits = ''.join(filter(str.isdigit, phone))
    
    # Remove country code if present
    if digits.startswith('972'):
        digits = digits[3:]
    
    # Must be 10 digits starting with 0
    if len(digits) != 10 or not digits.startswith('0'):
        return False
    
    # Valid prefixes for mobile: 050, 051, 052, 053, 054, 055, 058
    # Valid prefixes for landline: 02, 03, 04, 08, 09
    valid_mobile_prefixes = ['050', '051', '052', '053', '054', '055', '058']
    valid_landline_prefixes = ['02', '03', '04', '08', '09']
    
    prefix_3 = digits[:3]
    prefix_2 = digits[:2]
    
    return prefix_3 in valid_mobile_prefixes or prefix_2 in valid_landline_prefixes


def validate_business_id(business_id: str) -> bool:
    """
    Validate Israeli business ID (ח.ב / ע.מ)
    
    Args:
        business_id: Business ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Remove non-digits
    digits = ''.join(filter(str.isdigit, business_id))
    
    # Must be 9 digits
    if len(digits) != 9:
        return False
    
    # Use same Luhn algorithm as ID validation
    return validate_israeli_id(digits)


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "הסיסמה חייבת להכיל לפחות 8 תווים"
    
    if not re.search(r'[A-Z]', password):
        return False, "הסיסמה חייבת להכיל לפחות אות גדולה אחת"
    
    if not re.search(r'[a-z]', password):
        return False, "הסיסמה חייבת להכיל לפחות אות קטנה אחת"
    
    if not re.search(r'\d', password):
        return False, "הסיסמה חייבת להכיל לפחות ספרה אחת"
    
    return True, None
