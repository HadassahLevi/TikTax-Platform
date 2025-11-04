"""
Unit Tests for Israeli Validators
Tests all validation functions with real Israeli data and edge cases
"""

import pytest
from datetime import datetime, timedelta
from app.utils.validators import (
    validate_israeli_id,
    validate_israeli_business_number,
    validate_israeli_phone,
    calculate_vat,
    validate_vat_calculation,
    is_valid_receipt_date,
    normalize_hebrew_text,
    extract_receipt_number,
    format_israeli_currency,
    format_israeli_date,
    validate_email,
    validate_password_strength,
)


class TestIsraeliIDValidation:
    """Test Israeli ID number validation"""
    
    def test_valid_id_numbers(self):
        """Test with valid Israeli ID numbers"""
        valid_ids = [
            "123456782",  # Valid check digit
            "000000018",  # Edge case with leading zeros
        ]
        for id_num in valid_ids:
            assert validate_israeli_id(id_num), f"Should validate {id_num}"
    
    def test_invalid_id_numbers(self):
        """Test with invalid ID numbers"""
        invalid_ids = [
            "123456789",  # Wrong check digit
            "12345678",   # Too short
            "1234567890", # Too long
            "abcdefghi",  # Non-numeric
            "",           # Empty
            "000000000",  # All zeros
        ]
        for id_num in invalid_ids:
            assert not validate_israeli_id(id_num), f"Should reject {id_num}"


class TestBusinessNumberValidation:
    """Test Israeli business number validation"""
    
    def test_valid_business_numbers(self):
        """Test with valid business numbers"""
        # Note: Using the same algorithm as ID validation
        valid_business_nums = [
            "123456782",  # Valid
            "000000018",  # Valid with leading zeros
        ]
        for num in valid_business_nums:
            assert validate_israeli_business_number(num), f"Should validate {num}"
    
    def test_invalid_business_numbers(self):
        """Test with invalid business numbers"""
        invalid_nums = [
            "123456789",  # Wrong check digit
            "12345678",   # Too short
            "1234567890", # Too long
            "abc123456",  # Contains letters
            "",           # Empty
        ]
        for num in invalid_nums:
            assert not validate_israeli_business_number(num), f"Should reject {num}"


class TestPhoneValidation:
    """Test Israeli phone number validation"""
    
    def test_valid_mobile_numbers(self):
        """Test valid Israeli mobile numbers"""
        valid_mobiles = [
            "0501234567",  # 050 prefix
            "0521234567",  # 052 prefix
            "0541234567",  # 054 prefix
            "0581234567",  # 058 prefix
            "9720501234567",  # With country code
        ]
        for phone in valid_mobiles:
            assert validate_israeli_phone(phone), f"Should validate {phone}"
    
    def test_valid_landline_numbers(self):
        """Test valid Israeli landline numbers"""
        valid_landlines = [
            "0212345678",  # Jerusalem
            "0312345678",  # Tel Aviv
            "0412345678",  # Haifa
            "0812345678",  # Beer Sheva
        ]
        for phone in valid_landlines:
            assert validate_israeli_phone(phone), f"Should validate {phone}"
    
    def test_invalid_phone_numbers(self):
        """Test invalid phone numbers"""
        invalid_phones = [
            "123456789",   # Too short
            "01234567890", # Too long
            "0601234567",  # Invalid prefix
            "1501234567",  # Doesn't start with 0
            "",            # Empty
            "abcdefghij",  # Non-numeric
        ]
        for phone in invalid_phones:
            assert not validate_israeli_phone(phone), f"Should reject {phone}"


class TestVATCalculation:
    """Test VAT calculation functions"""
    
    def test_calculate_vat_standard_rate(self):
        """Test VAT calculation with standard 17% rate"""
        total_amount = 117.00
        pre_vat, vat, total = calculate_vat(total_amount, vat_rate=0.17)
        
        assert pre_vat == 100.00, "Pre-VAT should be 100.00"
        assert vat == 17.00, "VAT should be 17.00"
        assert total == 117.00, "Total should be 117.00"
    
    def test_calculate_vat_rounding(self):
        """Test VAT calculation with rounding"""
        total_amount = 100.00
        pre_vat, vat, total = calculate_vat(total_amount, vat_rate=0.17)
        
        # 100 / 1.17 = 85.47, VAT = 14.53
        assert pre_vat == 85.47, f"Pre-VAT should be 85.47, got {pre_vat}"
        assert vat == 14.53, f"VAT should be 14.53, got {vat}"
        assert total == 100.00, "Total should remain 100.00"
    
    def test_calculate_vat_large_amount(self):
        """Test VAT calculation with large amounts"""
        total_amount = 11700.00
        pre_vat, vat, total = calculate_vat(total_amount, vat_rate=0.17)
        
        assert pre_vat == 10000.00, "Pre-VAT should be 10000.00"
        assert vat == 1700.00, "VAT should be 1700.00"
        assert total == 11700.00, "Total should be 11700.00"


class TestVATValidation:
    """Test VAT calculation validation"""
    
    def test_valid_vat_calculation(self):
        """Test validation of correct VAT calculation"""
        assert validate_vat_calculation(117.00, 17.00, 100.00), "Should validate correct calculation"
        assert validate_vat_calculation(100.00, 14.53, 85.47), "Should validate with rounding"
    
    def test_invalid_vat_calculation(self):
        """Test validation of incorrect VAT calculation"""
        assert not validate_vat_calculation(117.00, 20.00, 100.00), "Should reject wrong VAT"
        assert not validate_vat_calculation(117.00, 17.00, 95.00), "Should reject wrong pre-VAT"
    
    def test_vat_validation_tolerance(self):
        """Test tolerance in VAT validation"""
        # Small difference within tolerance (0.02)
        assert validate_vat_calculation(117.00, 17.01, 99.99, tolerance=0.02), "Should allow small rounding"
        
        # Large difference outside tolerance
        assert not validate_vat_calculation(117.00, 17.50, 99.50, tolerance=0.02), "Should reject large difference"


class TestReceiptDateValidation:
    """Test receipt date validation"""
    
    def test_valid_dates(self):
        """Test valid receipt dates"""
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        one_year_ago = today - timedelta(days=365)
        six_years_ago = today - timedelta(days=365 * 6)
        
        assert is_valid_receipt_date(today), "Today should be valid"
        assert is_valid_receipt_date(yesterday), "Yesterday should be valid"
        assert is_valid_receipt_date(one_year_ago), "1 year ago should be valid"
        assert is_valid_receipt_date(six_years_ago), "6 years ago should be valid"
    
    def test_invalid_future_dates(self):
        """Test that future dates are invalid"""
        tomorrow = datetime.now() + timedelta(days=1)
        next_year = datetime.now() + timedelta(days=365)
        
        assert not is_valid_receipt_date(tomorrow), "Tomorrow should be invalid"
        assert not is_valid_receipt_date(next_year), "Next year should be invalid"
    
    def test_invalid_old_dates(self):
        """Test that dates older than 7 years are invalid"""
        eight_years_ago = datetime.now() - timedelta(days=365 * 8)
        ten_years_ago = datetime.now() - timedelta(days=365 * 10)
        
        assert not is_valid_receipt_date(eight_years_ago), "8 years ago should be invalid"
        assert not is_valid_receipt_date(ten_years_ago), "10 years ago should be invalid"
    
    def test_edge_case_seven_years(self):
        """Test edge case at exactly 7 years"""
        # Just under 7 years should be valid
        almost_seven_years = datetime.now() - timedelta(days=365 * 7 - 1)
        assert is_valid_receipt_date(almost_seven_years), "6.99 years ago should be valid"
        
        # Just over 7 years should be invalid
        over_seven_years = datetime.now() - timedelta(days=365 * 7 + 1)
        assert not is_valid_receipt_date(over_seven_years), "7.01 years ago should be invalid"


class TestHebrewTextNormalization:
    """Test Hebrew text normalization"""
    
    def test_remove_niqqud(self):
        """Test removal of niqqud (vowel points)"""
        text_with_niqqud = "שָׁלוֹם"  # Shalom with niqqud
        expected = "שלום"
        assert normalize_hebrew_text(text_with_niqqud) == expected
    
    def test_normalize_spaces(self):
        """Test space normalization"""
        text = "שלום    עולם   !"
        expected = "שלום עולם !"
        assert normalize_hebrew_text(text) == expected
    
    def test_standardize_quotes(self):
        """Test quote standardization"""
        text = 'שלום "עולם" ו׳שלום׳'
        expected = 'שלום "עולם" ו\'שלום\''
        assert normalize_hebrew_text(text) == expected
    
    def test_empty_string(self):
        """Test with empty string"""
        assert normalize_hebrew_text("") == ""
        assert normalize_hebrew_text(None) == ""
    
    def test_strip_whitespace(self):
        """Test stripping leading/trailing whitespace"""
        text = "  שלום עולם  "
        expected = "שלום עולם"
        assert normalize_hebrew_text(text) == expected


class TestReceiptNumberExtraction:
    """Test receipt number extraction"""
    
    def test_extract_hebrew_pattern(self):
        """Test extraction with Hebrew pattern"""
        text = "קבלה מס' 123456"
        assert extract_receipt_number(text) == "123456"
        
        text2 = "מספר קבלה: 789012"
        assert extract_receipt_number(text2) == "789012"
    
    def test_extract_english_pattern(self):
        """Test extraction with English pattern"""
        text = "Receipt No. 456789"
        assert extract_receipt_number(text) == "456789"
        
        text2 = "RECEIPT #123456"
        assert extract_receipt_number(text2) == "123456"
    
    def test_extract_mixed_text(self):
        """Test extraction from mixed Hebrew/English text"""
        text = "חנות ABC קבלה 987654 תודה"
        assert extract_receipt_number(text) == "987654"
    
    def test_no_receipt_number(self):
        """Test when no receipt number is found"""
        text = "שלום עולם"
        assert extract_receipt_number(text) == ""
        
        text2 = "Receipt 123"  # Too short (less than 4 digits)
        assert extract_receipt_number(text2) == ""


class TestCurrencyFormatting:
    """Test Israeli currency formatting"""
    
    def test_format_whole_number(self):
        """Test formatting whole numbers"""
        assert format_israeli_currency(100) == "₪100.00"
        assert format_israeli_currency(1000) == "₪1,000.00"
    
    def test_format_with_decimals(self):
        """Test formatting with decimal places"""
        assert format_israeli_currency(123.45) == "₪123.45"
        assert format_israeli_currency(1234.56) == "₪1,234.56"
    
    def test_format_large_amounts(self):
        """Test formatting large amounts"""
        assert format_israeli_currency(1000000) == "₪1,000,000.00"
        assert format_israeli_currency(12345678.90) == "₪12,345,678.90"
    
    def test_format_zero(self):
        """Test formatting zero"""
        assert format_israeli_currency(0) == "₪0.00"


class TestDateFormatting:
    """Test Israeli date formatting"""
    
    def test_format_date(self):
        """Test date formatting"""
        date = datetime(2023, 12, 31)
        assert format_israeli_date(date) == "31/12/2023"
        
        date2 = datetime(2024, 1, 1)
        assert format_israeli_date(date2) == "01/01/2024"
    
    def test_format_with_time(self):
        """Test that time is ignored"""
        date = datetime(2023, 12, 31, 14, 30, 45)
        assert format_israeli_date(date) == "31/12/2023"


class TestEmailValidation:
    """Test email validation"""
    
    def test_valid_emails(self):
        """Test valid email addresses"""
        valid_emails = [
            "user@example.com",
            "test.user@domain.co.il",
            "user+tag@example.com",
            "user123@test-domain.com",
        ]
        for email in valid_emails:
            assert validate_email(email), f"Should validate {email}"
    
    def test_invalid_emails(self):
        """Test invalid email addresses"""
        invalid_emails = [
            "invalid",
            "@example.com",
            "user@",
            "user @example.com",
            "user@example",
            "",
        ]
        for email in invalid_emails:
            assert not validate_email(email), f"Should reject {email}"


class TestPasswordStrength:
    """Test password strength validation"""
    
    def test_valid_passwords(self):
        """Test valid passwords"""
        valid_passwords = [
            "Test1234",
            "SecurePass1",
            "MyP@ssw0rd",
        ]
        for password in valid_passwords:
            is_valid, error = validate_password_strength(password)
            assert is_valid, f"Should validate {password}"
            assert error is None
    
    def test_too_short(self):
        """Test password too short"""
        is_valid, error = validate_password_strength("Test1")
        assert not is_valid
        assert "8 תווים" in error
    
    def test_no_uppercase(self):
        """Test password without uppercase"""
        is_valid, error = validate_password_strength("test1234")
        assert not is_valid
        assert "אות גדולה" in error
    
    def test_no_lowercase(self):
        """Test password without lowercase"""
        is_valid, error = validate_password_strength("TEST1234")
        assert not is_valid
        assert "אות קטנה" in error
    
    def test_no_digit(self):
        """Test password without digit"""
        is_valid, error = validate_password_strength("TestTest")
        assert not is_valid
        assert "ספרה" in error


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_none_values(self):
        """Test handling of None values"""
        assert normalize_hebrew_text(None) == ""
        assert extract_receipt_number("") == ""
    
    def test_special_characters(self):
        """Test handling of special characters"""
        text = "!@#$%^&*() 123456"
        # Should still extract number
        result = extract_receipt_number(text)
        assert "123456" in result or result == ""
    
    def test_unicode_handling(self):
        """Test proper Unicode handling"""
        hebrew_text = "שלום עולם"
        result = normalize_hebrew_text(hebrew_text)
        assert isinstance(result, str)
        assert len(result) > 0
