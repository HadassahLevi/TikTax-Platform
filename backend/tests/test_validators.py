import pytest
from app.utils.validators import (
    validate_israeli_id,
    validate_israeli_business_number,
    validate_israeli_phone,
    validate_vat_calculation,
    is_valid_receipt_date,
)
from datetime import datetime, timedelta


def test_validate_israeli_id_valid():
    """Test valid Israeli ID numbers"""
    # These are valid IDs that pass Luhn checksum
    assert validate_israeli_id("123456783") == True  # Valid ID (checksum digit = 3)
    assert validate_israeli_id("305219892") == True  # Valid ID (checksum digit = 2)
    assert validate_israeli_id("111111114") == True  # Valid ID (checksum digit = 4)


def test_validate_israeli_id_invalid():
    """Test invalid Israeli ID numbers"""
    assert validate_israeli_id("123456789") == False  # Invalid checksum
    assert validate_israeli_id("123456788") == False  # Invalid checksum
    assert validate_israeli_id("12345678") == False   # Too short
    assert validate_israeli_id("1234567890") == False # Too long


def test_validate_business_number_valid():
    """Test valid business numbers"""
    # Valid business numbers that pass Luhn checksum
    assert validate_israeli_business_number("123456783") == True  # Valid checksum
    assert validate_israeli_business_number("305219892") == True  # Valid checksum


def test_validate_business_number_invalid():
    """Test invalid business numbers"""
    assert validate_israeli_business_number("123456789") == False  # Invalid checksum
    assert validate_israeli_business_number("123") == False  # Too short


def test_validate_israeli_phone_valid():
    """Test valid Israeli phone numbers"""
    # Must be 10 digits starting with 0
    assert validate_israeli_phone("0501234567") == True  # Mobile
    assert validate_israeli_phone("050-123-4567") == True  # Mobile with dashes
    assert validate_israeli_phone("0509876543") == True  # Mobile
    assert validate_israeli_phone("021234567") == False  # Landline needs full 10 digits
    assert validate_israeli_phone("0212345678") == True  # Valid landline


def test_validate_israeli_phone_invalid():
    """Test invalid Israeli phone numbers"""
    assert validate_israeli_phone("+1234567890") == False  # Wrong country
    assert validate_israeli_phone("123") == False  # Too short
    assert validate_israeli_phone("1501234567") == False  # Doesn't start with 0


def test_validate_vat_calculation_valid():
    """Test VAT calculation validation"""
    # Valid: pre_vat + vat = total
    assert validate_vat_calculation(total=117.0, vat=17.0, pre_vat=100.0, tolerance=1.0) == True
    assert validate_vat_calculation(total=118.0, vat=18.0, pre_vat=100.0, tolerance=1.0) == True


def test_validate_vat_calculation_invalid():
    """Test invalid VAT calculation"""
    # Invalid: pre_vat + vat != total (outside tolerance)
    assert validate_vat_calculation(total=200.0, vat=17.0, pre_vat=100.0, tolerance=1.0) == False
    assert validate_vat_calculation(total=50.0, vat=18.0, pre_vat=100.0, tolerance=1.0) == False


def test_validate_receipt_date_valid():
    """Test valid receipt dates"""
    today = datetime.now()
    assert is_valid_receipt_date(today) == True
    
    # 6 years ago (within 7-year limit)
    six_years_ago = today - timedelta(days=365*6)
    assert is_valid_receipt_date(six_years_ago) == True


def test_validate_receipt_date_invalid():
    """Test invalid receipt dates"""
    # Future date
    future = datetime.now() + timedelta(days=1)
    assert is_valid_receipt_date(future) == False
    
    # 8 years ago (beyond 7-year limit)
    eight_years_ago = datetime.now() - timedelta(days=365*8)
    assert is_valid_receipt_date(eight_years_ago) == False

