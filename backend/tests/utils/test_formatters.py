"""
Unit Tests for Israeli Formatters
Tests all formatting functions with real Israeli data
"""

import pytest
from datetime import datetime
from app.utils.formatters import (
    format_israeli_currency,
    format_israeli_phone,
    format_israeli_date,
    format_business_id,
    format_amount,
    format_phone_display,
    format_business_number,
    parse_date_flexible,
    calculate_vat,
    calculate_total_with_vat,
)


class TestCurrencyFormatting:
    """Test Israeli currency formatting"""
    
    def test_format_whole_numbers(self):
        """Test formatting whole numbers"""
        assert format_israeli_currency(100) == "₪100.00"
        assert format_israeli_currency(1000) == "₪1,000.00"
        assert format_israeli_currency(10000) == "₪10,000.00"
    
    def test_format_with_decimals(self):
        """Test formatting with decimal places"""
        assert format_israeli_currency(123.45) == "₪123.45"
        assert format_israeli_currency(1234.56) == "₪1,234.56"
        assert format_israeli_currency(12345.67) == "₪12,345.67"
    
    def test_format_large_amounts(self):
        """Test formatting large amounts with commas"""
        assert format_israeli_currency(1000000) == "₪1,000,000.00"
        assert format_israeli_currency(12345678.90) == "₪12,345,678.90"
    
    def test_format_small_amounts(self):
        """Test formatting small amounts"""
        assert format_israeli_currency(0.50) == "₪0.50"
        assert format_israeli_currency(1.99) == "₪1.99"
    
    def test_format_zero(self):
        """Test formatting zero"""
        assert format_israeli_currency(0) == "₪0.00"


class TestPhoneFormatting:
    """Test Israeli phone number formatting"""
    
    def test_format_mobile_numbers(self):
        """Test formatting Israeli mobile numbers"""
        assert format_israeli_phone("0501234567") == "050-123-4567"
        assert format_israeli_phone("0521234567") == "052-123-4567"
        assert format_israeli_phone("0541234567") == "054-123-4567"
    
    def test_format_landline_numbers(self):
        """Test formatting Israeli landline numbers"""
        assert format_israeli_phone("0212345678") == "021-234-5678"
        assert format_israeli_phone("0312345678") == "031-234-5678"
    
    def test_format_with_country_code(self):
        """Test formatting numbers with country code"""
        # Should remove country code and format
        assert format_israeli_phone("9720501234567") == "050-123-4567"
        assert format_israeli_phone("9720521234567") == "052-123-4567"
    
    def test_format_already_formatted(self):
        """Test formatting already formatted numbers"""
        # Should handle numbers with non-digits
        result = format_israeli_phone("050-123-4567")
        assert result == "050-123-4567"
    
    def test_format_invalid_length(self):
        """Test formatting numbers with invalid length"""
        # Should return original if can't format
        assert format_israeli_phone("123") == "123"
        assert format_israeli_phone("12345678901234") == "12345678901234"


class TestPhoneDisplay:
    """Test phone display formatting"""
    
    def test_format_international_to_local(self):
        """Test converting international format to local display"""
        assert format_phone_display("+972501234567") == "050-123-4567"
        assert format_phone_display("972501234567") == "050-123-4567"
    
    def test_format_local_numbers(self):
        """Test formatting local numbers"""
        assert format_phone_display("0501234567") == "050-123-4567"
        assert format_phone_display("0521234567") == "052-123-4567"
    
    def test_preserve_invalid_format(self):
        """Test that invalid formats are preserved"""
        assert format_phone_display("123") == "123"
        assert format_phone_display("invalid") == "invalid"


class TestDateFormatting:
    """Test Israeli date formatting"""
    
    def test_format_standard_dates(self):
        """Test formatting standard dates"""
        date = datetime(2023, 12, 31)
        assert format_israeli_date(date) == "31/12/2023"
        
        date2 = datetime(2024, 1, 1)
        assert format_israeli_date(date2) == "01/01/2024"
    
    def test_format_with_leading_zeros(self):
        """Test formatting dates with leading zeros"""
        date = datetime(2023, 1, 5)
        assert format_israeli_date(date) == "05/01/2023"
    
    def test_ignore_time_component(self):
        """Test that time component is ignored"""
        date = datetime(2023, 12, 31, 14, 30, 45)
        assert format_israeli_date(date) == "31/12/2023"


class TestBusinessNumberFormatting:
    """Test business number formatting"""
    
    def test_format_valid_business_number(self):
        """Test formatting valid 9-digit business numbers"""
        assert format_business_id("123456789") == "123-456-789"
        assert format_business_number("123456789") == "12-345-6789"
    
    def test_format_with_non_digits(self):
        """Test formatting numbers with non-digits"""
        # Should remove non-digits first
        result = format_business_id("12-34-56-789")
        assert result == "123-456-789"
    
    def test_format_invalid_length(self):
        """Test formatting numbers with invalid length"""
        # Should return original if not 9 digits
        assert format_business_id("12345") == "12345"
        assert format_business_id("1234567890") == "1234567890"


class TestAmountFormatting:
    """Test amount formatting"""
    
    def test_format_valid_amounts(self):
        """Test formatting valid amounts"""
        assert format_amount(100.00) == "100.00"
        assert format_amount(123.45) == "123.45"
        assert format_amount(1234.56) == "1234.56"
    
    def test_format_none(self):
        """Test formatting None value"""
        assert format_amount(None) == "0.00"
    
    def test_format_zero(self):
        """Test formatting zero"""
        assert format_amount(0) == "0.00"
        assert format_amount(0.00) == "0.00"
    
    def test_format_rounding(self):
        """Test that formatting rounds to 2 decimals"""
        assert format_amount(123.456) == "123.46"
        assert format_amount(123.454) == "123.45"


class TestDateParsing:
    """Test flexible date parsing"""
    
    def test_parse_israeli_format(self):
        """Test parsing DD/MM/YYYY format"""
        date = parse_date_flexible("31/12/2023")
        assert date is not None
        assert date.year == 2023
        assert date.month == 12
        assert date.day == 31
    
    def test_parse_iso_format(self):
        """Test parsing YYYY-MM-DD format"""
        date = parse_date_flexible("2023-12-31")
        assert date is not None
        assert date.year == 2023
        assert date.month == 12
        assert date.day == 31
    
    def test_parse_dot_format(self):
        """Test parsing DD.MM.YYYY format"""
        date = parse_date_flexible("31.12.2023")
        assert date is not None
        assert date.year == 2023
        assert date.month == 12
        assert date.day == 31
    
    def test_parse_dash_format(self):
        """Test parsing DD-MM-YYYY format"""
        date = parse_date_flexible("31-12-2023")
        assert date is not None
        assert date.year == 2023
        assert date.month == 12
        assert date.day == 31
    
    def test_parse_short_year(self):
        """Test parsing with 2-digit year"""
        date = parse_date_flexible("31/12/23")
        assert date is not None
        assert date.year == 2023
        assert date.month == 12
        assert date.day == 31
    
    def test_parse_with_spaces(self):
        """Test parsing with leading/trailing spaces"""
        date = parse_date_flexible("  31/12/2023  ")
        assert date is not None
        assert date.year == 2023
    
    def test_parse_invalid_format(self):
        """Test parsing invalid format returns None"""
        assert parse_date_flexible("invalid") is None
        assert parse_date_flexible("32/13/2023") is None
        assert parse_date_flexible("") is None
    
    def test_parse_ambiguous_dates(self):
        """Test parsing potentially ambiguous dates"""
        # 01/02/2023 could be Feb 1 or Jan 2
        # Our parser treats it as DD/MM/YYYY, so Feb 1
        date = parse_date_flexible("01/02/2023")
        assert date is not None
        assert date.day == 1
        assert date.month == 2


class TestVATCalculation:
    """Test VAT calculation functions"""
    
    def test_calculate_vat_from_total(self):
        """Test calculating VAT from total amount"""
        vat = calculate_vat(117.00)
        assert vat == 17.00
        
        vat2 = calculate_vat(100.00)
        assert vat2 == 14.53
    
    def test_calculate_vat_custom_rate(self):
        """Test calculating VAT with custom rate"""
        # 18% rate
        vat = calculate_vat(118.00, vat_rate=0.18)
        assert vat == 18.00
    
    def test_calculate_total_with_vat(self):
        """Test calculating total from pre-VAT amount"""
        total = calculate_total_with_vat(100.00)
        assert total == 117.00
        
        total2 = calculate_total_with_vat(85.47)
        assert total2 == 100.00
    
    def test_calculate_total_custom_rate(self):
        """Test calculating total with custom VAT rate"""
        # 18% rate
        total = calculate_total_with_vat(100.00, vat_rate=0.18)
        assert total == 118.00
    
    def test_vat_roundtrip(self):
        """Test that VAT calculation is consistent"""
        # Start with pre-VAT amount
        pre_vat = 100.00
        
        # Calculate total
        total = calculate_total_with_vat(pre_vat)
        assert total == 117.00
        
        # Calculate VAT from total
        vat = calculate_vat(total)
        assert vat == 17.00
        
        # Verify: pre_vat + vat = total
        assert pre_vat + vat == total


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_strings(self):
        """Test handling empty strings"""
        assert format_israeli_phone("") == ""
        assert format_business_id("") == ""
    
    def test_very_large_amounts(self):
        """Test formatting very large amounts"""
        result = format_israeli_currency(999999999.99)
        assert "₪" in result
        assert "999,999,999.99" in result
    
    def test_negative_amounts(self):
        """Test formatting negative amounts"""
        result = format_israeli_currency(-100.00)
        assert "₪-100.00" in result
    
    def test_special_characters_in_phone(self):
        """Test phone formatting with special characters"""
        # Should strip special characters
        result = format_israeli_phone("050-123-4567")
        assert result == "050-123-4567"
        
        result2 = format_israeli_phone("(050) 123-4567")
        assert "050" in result2
    
    def test_whitespace_in_dates(self):
        """Test date parsing with extra whitespace"""
        date = parse_date_flexible("  31 / 12 / 2023  ")
        # May fail due to spaces within date, which is expected
        # Our parser expects clean format
        assert date is None  # Expected to fail
        
        # But should work with trim
        date2 = parse_date_flexible("31/12/2023  ")
        assert date2 is not None


class TestRealWorldScenarios:
    """Test with real-world Israeli data"""
    
    def test_typical_receipt_amounts(self):
        """Test formatting typical receipt amounts"""
        # Coffee shop
        assert format_israeli_currency(18.50) == "₪18.50"
        
        # Restaurant
        assert format_israeli_currency(342.00) == "₪342.00"
        
        # Gas station
        assert format_israeli_currency(456.78) == "₪456.78"
        
        # Office supplies
        assert format_israeli_currency(1250.00) == "₪1,250.00"
    
    def test_typical_business_numbers(self):
        """Test formatting typical business numbers"""
        # Format as XXX-XXX-XXX
        assert format_business_id("514123456") == "514-123-456"
        assert format_business_id("580123456") == "580-123-456"
    
    def test_typical_phone_numbers(self):
        """Test formatting typical Israeli phone numbers"""
        # Mobile numbers
        assert format_israeli_phone("0501234567") == "050-123-4567"
        assert format_israeli_phone("0521234567") == "052-123-4567"
        
        # Landlines
        assert format_israeli_phone("0236543210") == "023-654-3210"
        assert format_israeli_phone("0391234567") == "039-123-4567"
    
    def test_typical_vat_calculations(self):
        """Test VAT calculations with typical amounts"""
        # Small purchase
        pre_vat, vat, total = (10.00, 1.70, 11.70)
        calculated_total = calculate_total_with_vat(pre_vat)
        assert calculated_total == total
        
        # Medium purchase
        pre_vat2, vat2, total2 = (100.00, 17.00, 117.00)
        calculated_total2 = calculate_total_with_vat(pre_vat2)
        assert calculated_total2 == total2
        
        # Large purchase
        pre_vat3, vat3, total3 = (1000.00, 170.00, 1170.00)
        calculated_total3 = calculate_total_with_vat(pre_vat3)
        assert calculated_total3 == total3
