"""
Israeli Format Helpers
Utilities for formatting Israeli-specific data
"""

from datetime import datetime
from typing import Optional


def format_israeli_currency(amount: float) -> str:
    """
    Format amount as Israeli currency
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted string (e.g., "₪1,234.56")
    """
    return f"₪{amount:,.2f}"


def format_israeli_phone(phone: str) -> str:
    """
    Format Israeli phone number
    
    Args:
        phone: Phone number
        
    Returns:
        Formatted phone (e.g., "050-123-4567")
    """
    # Remove non-digits
    digits = ''.join(filter(str.isdigit, phone))
    
    # Remove country code if present
    if digits.startswith('972'):
        digits = '0' + digits[3:]
    
    # Format as 0XX-XXX-XXXX
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    
    return phone


def format_israeli_date(date: datetime) -> str:
    """
    Format date in Israeli format (DD/MM/YYYY)
    
    Args:
        date: Datetime to format
        
    Returns:
        Formatted date string
    """
    return date.strftime("%d/%m/%Y")


def format_business_id(business_id: str) -> str:
    """
    Format Israeli business ID (ח.ב / ע.מ)
    
    Args:
        business_id: Business ID
        
    Returns:
        Formatted business ID
    """
    # Remove non-digits
    digits = ''.join(filter(str.isdigit, business_id))
    
    # Add dashes for readability
    if len(digits) == 9:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    
    return business_id


def calculate_vat(amount: float, vat_rate: float = 0.17) -> float:
    """
    Calculate VAT amount from total
    
    Args:
        amount: Total amount including VAT
        vat_rate: VAT rate (default 17%)
        
    Returns:
        VAT amount
    """
    return round(amount * (vat_rate / (1 + vat_rate)), 2)


def calculate_total_with_vat(amount: float, vat_rate: float = 0.17) -> float:
    """
    Calculate total including VAT
    
    Args:
        amount: Amount before VAT
        vat_rate: VAT rate (default 17%)
        
    Returns:
        Total including VAT
    """
    return round(amount * (1 + vat_rate), 2)


def format_amount(amount: Optional[float]) -> str:
    """
    Format amount with 2 decimal places
    
    Args:
        amount: Amount to format (can be None)
    
    Returns:
        Formatted amount string
    """
    if amount is None:
        return "0.00"
    return f"{amount:.2f}"


def format_phone_display(phone: str) -> str:
    """
    Format Israeli phone for display
    Converts international format to local display format
    
    Args:
        phone: Phone number (e.g., "+972501234567" or "0501234567")
    
    Returns:
        Formatted phone (e.g., "050-123-4567")
    """
    # Remove all non-digits
    digits = ''.join(filter(str.isdigit, phone))
    
    # Convert international to local
    if digits.startswith('972'):
        digits = '0' + digits[3:]
    
    # Format as XXX-XXX-XXXX
    if len(digits) == 10 and digits.startswith('0'):
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    
    return phone


def format_business_number(business_num: str) -> str:
    """
    Format business number for display
    
    Args:
        business_num: Business number (9 digits)
    
    Returns:
        Formatted business number (e.g., "12-345-6789")
    """
    # Remove non-digits
    digits = ''.join(filter(str.isdigit, business_num))
    
    if len(digits) == 9:
        return f"{digits[:2]}-{digits[2:5]}-{digits[5:]}"
    return business_num


def parse_date_flexible(date_str: str) -> Optional[datetime]:
    """
    Parse date from various formats
    Handles: DD/MM/YYYY, YYYY-MM-DD, DD.MM.YYYY, etc.
    
    Args:
        date_str: Date string in various formats
    
    Returns:
        Parsed datetime or None if parsing fails
    """
    formats = [
        "%d/%m/%Y",      # 31/12/2023
        "%Y-%m-%d",      # 2023-12-31
        "%d.%m.%Y",      # 31.12.2023
        "%d-%m-%Y",      # 31-12-2023
        "%Y/%m/%d",      # 2023/12/31
        "%d/%m/%y",      # 31/12/23
        "%d.%m.%y",      # 31.12.23
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    
    return None
