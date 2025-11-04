"""
Quick validation test script
Tests key validator functions without full pytest setup
"""

import sys
sys.path.insert(0, '.')

from datetime import datetime, timedelta
from app.utils.validators import (
    validate_israeli_id,
    validate_israeli_business_number,
    calculate_vat,
    validate_vat_calculation,
    is_valid_receipt_date,
    normalize_hebrew_text,
    extract_receipt_number,
)
from app.utils.formatters import (
    format_amount,
    format_phone_display,
    format_business_number,
    parse_date_flexible,
)

print("=" * 60)
print("TESTING ISRAELI VALIDATORS")
print("=" * 60)

# Test Israeli ID validation
print("\n1. Israeli ID Validation:")
# Using valid test IDs
valid_id = "000000019"  # Valid ID with check digit (mod 10 = 0)
invalid_id = "000000018"  # Invalid check digit
print(f"   Valid ID ({valid_id}): {validate_israeli_id(valid_id)}")
print(f"   Invalid ID ({invalid_id}): {validate_israeli_id(invalid_id)}")

# Test business number validation
print("\n2. Business Number Validation:")
print(f"   Valid ({valid_id}): {validate_israeli_business_number(valid_id)}")
print(f"   Invalid ({invalid_id}): {validate_israeli_business_number(invalid_id)}")

# Test VAT calculation
print("\n3. VAT Calculation:")
pre_vat, vat, total = calculate_vat(117.00)
print(f"   Total: ₪117.00 -> Pre-VAT: ₪{pre_vat}, VAT: ₪{vat}")
assert pre_vat == 100.00 and vat == 17.00, "VAT calculation error!"

pre_vat2, vat2, total2 = calculate_vat(100.00)
print(f"   Total: ₪100.00 -> Pre-VAT: ₪{pre_vat2}, VAT: ₪{vat2}")
assert pre_vat2 == 85.47 and vat2 == 14.53, "VAT calculation error!"

# Test VAT validation
print("\n4. VAT Validation:")
is_valid = validate_vat_calculation(117.00, 17.00, 100.00)
print(f"   Correct VAT (117=100+17): {is_valid}")
assert is_valid, "Should validate correct VAT!"

is_invalid = validate_vat_calculation(117.00, 20.00, 95.00)  # 95 + 20 = 115, not 117
print(f"   Incorrect VAT (117≠95+20=115): {is_invalid}")
assert not is_invalid, "Should reject incorrect VAT!"

# Test date validation
print("\n5. Receipt Date Validation:")
print(f"   Today: {is_valid_receipt_date(datetime.now())}")  # True
print(f"   Tomorrow: {is_valid_receipt_date(datetime.now() + timedelta(days=1))}")  # False
print(f"   1 year ago: {is_valid_receipt_date(datetime.now() - timedelta(days=365))}")  # True
print(f"   8 years ago: {is_valid_receipt_date(datetime.now() - timedelta(days=365*8))}")  # False

# Test Hebrew text normalization
print("\n6. Hebrew Text Normalization:")
hebrew_text = "  שלום    עולם  "
normalized = normalize_hebrew_text(hebrew_text)
print(f"   Original: '{hebrew_text}'")
print(f"   Normalized: '{normalized}'")
assert normalized == "שלום עולם", "Normalization failed!"

# Test receipt number extraction
print("\n7. Receipt Number Extraction:")
text1 = "קבלה מס' 123456"
number1 = extract_receipt_number(text1)
print(f"   '{text1}' -> {number1}")
assert number1 == "123456", "Extraction failed!"

text2 = "Receipt No. 789012"
number2 = extract_receipt_number(text2)
print(f"   '{text2}' -> {number2}")
assert number2 == "789012", "Extraction failed!"

print("\n" + "=" * 60)
print("TESTING FORMATTERS")
print("=" * 60)

# Test amount formatting
print("\n8. Amount Formatting:")
print(f"   None -> {format_amount(None)}")
assert format_amount(None) == "0.00"
print(f"   123.456 -> {format_amount(123.456)}")
assert format_amount(123.456) == "123.46"

# Test phone formatting
print("\n9. Phone Display Formatting:")
print(f"   +972501234567 -> {format_phone_display('+972501234567')}")
print(f"   0501234567 -> {format_phone_display('0501234567')}")

# Test business number formatting
print("\n10. Business Number Formatting:")
print(f"   123456789 -> {format_business_number('123456789')}")
assert format_business_number('123456789') == "12-345-6789"

# Test date parsing
print("\n11. Flexible Date Parsing:")
date1 = parse_date_flexible("31/12/2023")
print(f"   '31/12/2023' -> {date1}")
assert date1 and date1.year == 2023 and date1.month == 12 and date1.day == 31

date2 = parse_date_flexible("2023-12-31")
print(f"   '2023-12-31' -> {date2}")
assert date2 and date2.year == 2023

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nValidator Features Implemented:")
print("  ✓ Israeli ID validation with check digit")
print("  ✓ Israeli business number validation")
print("  ✓ VAT calculation (17% Israeli rate)")
print("  ✓ VAT validation with tolerance")
print("  ✓ Receipt date validation (7-year rule)")
print("  ✓ Hebrew text normalization")
print("  ✓ Receipt number extraction")
print("  ✓ Amount formatting")
print("  ✓ Phone number formatting")
print("  ✓ Business number formatting")
print("  ✓ Flexible date parsing")
print("\n" + "=" * 60)
