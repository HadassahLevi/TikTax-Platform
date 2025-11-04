"""
Standalone Receipt Validation Demonstration
Shows validation without requiring database or external services
"""

import sys
sys.path.insert(0, '.')

from datetime import datetime, timedelta
from typing import Tuple, List
from app.utils.validators import (
    validate_israeli_business_number,
    validate_vat_calculation,
    calculate_vat,
    is_valid_receipt_date,
)


class MockReceipt:
    """Mock receipt for demonstration"""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.user_id = kwargs.get('user_id')
        self.vendor_name = kwargs.get('vendor_name')
        self.business_number = kwargs.get('business_number')
        self.receipt_date = kwargs.get('receipt_date')
        self.total_amount = kwargs.get('total_amount')
        self.vat_amount = kwargs.get('vat_amount')
        self.pre_vat_amount = kwargs.get('pre_vat_amount')
        self.confidence_score = kwargs.get('confidence_score')
        self.ocr_data = kwargs.get('ocr_data')


def validate_receipt_data(receipt: MockReceipt) -> Tuple[bool, List[str]]:
    """Validate receipt data (standalone version)"""
    warnings = []
    
    # Validate business number
    if receipt.business_number:
        if not validate_israeli_business_number(receipt.business_number):
            warnings.append("מספר עוסק מורשה לא תקין")
    
    # Validate date
    if receipt.receipt_date:
        if not is_valid_receipt_date(receipt.receipt_date):
            if receipt.receipt_date > datetime.now():
                warnings.append("תאריך הקבלה בעתיד - לא חוקי")
            else:
                warnings.append("תאריך הקבלה ישן מדי (מעל 7 שנים)")
    
    # Validate VAT calculation
    if all([receipt.total_amount, receipt.vat_amount, receipt.pre_vat_amount]):
        if not validate_vat_calculation(
            receipt.total_amount,
            receipt.vat_amount,
            receipt.pre_vat_amount
        ):
            warnings.append("חישוב מע״מ לא מדויק - נדרש אימות")
    
    # Check confidence scores
    if receipt.ocr_data and receipt.ocr_data.get("parsed_data"):
        parsed_data = receipt.ocr_data["parsed_data"]
        if "confidence" in parsed_data:
            confidences = parsed_data["confidence"]
            low_confidence_fields = [
                field for field, conf in confidences.items()
                if conf < 0.7
            ]
            if low_confidence_fields:
                field_names_hebrew = {
                    "vendor_name": "שם העסק",
                    "total_amount": "סכום כולל",
                    "receipt_date": "תאריך",
                    "business_number": "ח.פ",
                    "vat_amount": "מע״מ",
                }
                hebrew_fields = [
                    field_names_hebrew.get(f, f) for f in low_confidence_fields
                ]
                warnings.append(f"דיוק נמוך בשדות: {', '.join(hebrew_fields)}")
    
    # Check for missing critical fields
    if not receipt.vendor_name:
        warnings.append("חסר שם עסק")
    
    if not receipt.total_amount or receipt.total_amount <= 0:
        warnings.append("סכום לא תקין")
    
    if not receipt.receipt_date:
        warnings.append("חסר תאריך קבלה")
    
    is_valid = len(warnings) == 0
    return is_valid, warnings


def recalculate_vat(receipt: MockReceipt) -> None:
    """Recalculate VAT from total"""
    if receipt.total_amount and receipt.total_amount > 0:
        pre_vat, vat, total = calculate_vat(receipt.total_amount)
        receipt.pre_vat_amount = pre_vat
        receipt.vat_amount = vat


def demo_receipt_validation():
    """Demonstrate receipt validation with various scenarios"""
    
    print("=" * 70)
    print("RECEIPT VALIDATION SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # Scenario 1: Perfect Receipt
    print("\n📋 Scenario 1: Perfect Coffee Shop Receipt")
    print("-" * 70)
    receipt1 = MockReceipt(
        id=1,
        user_id="user123",
        vendor_name="קפה אומה",
        business_number="000000019",  # Valid check digit
        receipt_date=datetime.now() - timedelta(hours=2),
        total_amount=18.50,
        vat_amount=2.68,
        pre_vat_amount=15.82,
        confidence_score=0.95,
    )
    
    is_valid, warnings = validate_receipt_data(receipt1)
    print(f"Vendor: {receipt1.vendor_name}")
    print(f"Amount: ₪{receipt1.total_amount:.2f}")
    print(f"Date: {receipt1.receipt_date.strftime('%d/%m/%Y %H:%M')}")
    print(f"Business #: {receipt1.business_number}")
    print(f"✅ Valid: {is_valid}")
    if warnings:
        print(f"⚠️  Warnings: {', '.join(warnings)}")
    else:
        print("✓ No warnings - perfect receipt!")
    
    # Scenario 2: Invalid Business Number
    print("\n\n📋 Scenario 2: Receipt with Invalid Business Number")
    print("-" * 70)
    receipt2 = MockReceipt(
        id=2,
        user_id="user123",
        vendor_name="מסעדת הבשר",
        business_number="123456789",  # Invalid check digit
        receipt_date=datetime.now() - timedelta(days=1),
        total_amount=580.00,
    )
    
    recalculate_vat(receipt2)
    is_valid, warnings = validate_receipt_data(receipt2)
    
    print(f"Vendor: {receipt2.vendor_name}")
    print(f"Amount: ₪{receipt2.total_amount:.2f}")
    print(f"VAT: ₪{receipt2.vat_amount:.2f} (auto-calculated)")
    print(f"Pre-VAT: ₪{receipt2.pre_vat_amount:.2f}")
    print(f"Business #: {receipt2.business_number}")
    print(f"❌ Valid: {is_valid}")
    print(f"⚠️  Warnings:")
    for warning in warnings:
        print(f"   - {warning}")
    
    # Scenario 3: Future Date (Invalid)
    print("\n\n📋 Scenario 3: Receipt with Future Date")
    print("-" * 70)
    receipt3 = MockReceipt(
        id=3,
        user_id="user123",
        vendor_name="שופרסל",
        receipt_date=datetime.now() + timedelta(days=1),  # Tomorrow!
        total_amount=342.50,
    )
    
    is_valid, warnings = validate_receipt_data(receipt3)
    
    print(f"Vendor: {receipt3.vendor_name}")
    print(f"Amount: ₪{receipt3.total_amount:.2f}")
    print(f"Date: {receipt3.receipt_date.strftime('%d/%m/%Y')}")
    print(f"❌ Valid: {is_valid}")
    print(f"⚠️  Warnings:")
    for warning in warnings:
        print(f"   - {warning}")
    
    # Scenario 4: Old Receipt (>7 years)
    print("\n\n📋 Scenario 4: Receipt Older than 7 Years")
    print("-" * 70)
    receipt4 = MockReceipt(
        id=4,
        user_id="user123",
        vendor_name="דלק",
        receipt_date=datetime.now() - timedelta(days=365 * 8),  # 8 years ago
        total_amount=456.78,
    )
    
    is_valid, warnings = validate_receipt_data(receipt4)
    
    print(f"Vendor: {receipt4.vendor_name}")
    print(f"Amount: ₪{receipt4.total_amount:.2f}")
    print(f"Date: {receipt4.receipt_date.strftime('%d/%m/%Y')} (8 years ago)")
    print(f"❌ Valid: {is_valid}")
    print(f"⚠️  Warnings:")
    for warning in warnings:
        print(f"   - {warning}")
    
    # Scenario 5: Low OCR Confidence
    print("\n\n📋 Scenario 5: Receipt with Low OCR Confidence")
    print("-" * 70)
    receipt5 = MockReceipt(
        id=5,
        user_id="user123",
        vendor_name="מאפיה",
        receipt_date=datetime.now() - timedelta(hours=3),
        total_amount=45.00,
        ocr_data={
            "success": True,
            "parsed_data": {
                "vendor_name": "מאפיה",
                "total_amount": 45.00,
                "confidence": {
                    "vendor_name": 0.95,
                    "total_amount": 0.55,  # Low confidence!
                    "receipt_date": 0.62,  # Low confidence!
                }
            }
        }
    )
    
    is_valid, warnings = validate_receipt_data(receipt5)
    
    print(f"Vendor: {receipt5.vendor_name}")
    print(f"Amount: ₪{receipt5.total_amount:.2f}")
    print(f"OCR Confidence:")
    for field, conf in receipt5.ocr_data["parsed_data"]["confidence"].items():
        status = "✓" if conf >= 0.7 else "⚠️ "
        print(f"   {status} {field}: {conf:.0%}")
    print(f"❌ Valid: {is_valid}")
    print(f"⚠️  Warnings:")
    for warning in warnings:
        print(f"   - {warning}")
    
    # Scenario 6: Missing Critical Fields
    print("\n\n📋 Scenario 6: Receipt with Missing Fields")
    print("-" * 70)
    receipt6 = MockReceipt(
        id=6,
        user_id="user123",
        # vendor_name missing!
        # receipt_date missing!
        total_amount=0,  # Invalid amount!
    )
    
    is_valid, warnings = validate_receipt_data(receipt6)
    
    print(f"Vendor: {receipt6.vendor_name or '[MISSING]'}")
    print(f"Amount: ₪{receipt6.total_amount:.2f}")
    print(f"Date: {receipt6.receipt_date or '[MISSING]'}")
    print(f"❌ Valid: {is_valid}")
    print(f"⚠️  Warnings ({len(warnings)} issues):")
    for warning in warnings:
        print(f"   - {warning}")
    
    # Scenario 7: Perfect Supermarket Receipt
    print("\n\n📋 Scenario 7: Perfect Supermarket Receipt (Auto VAT)")
    print("-" * 70)
    receipt7 = MockReceipt(
        id=7,
        user_id="user123",
        vendor_name="רמי לוי",
        business_number="000000019",
        receipt_date=datetime.now() - timedelta(days=2),
        total_amount=234.00,
        # No VAT data - will be calculated
    )
    
    # Auto-calculate VAT
    recalculate_vat(receipt7)
    is_valid, warnings = validate_receipt_data(receipt7)
    
    print(f"Vendor: {receipt7.vendor_name}")
    print(f"Amount: ₪{receipt7.total_amount:.2f}")
    print(f"VAT Breakdown:")
    print(f"   Pre-VAT: ₪{receipt7.pre_vat_amount:.2f}")
    print(f"   VAT (17%): ₪{receipt7.vat_amount:.2f}")
    print(f"   Total: ₪{receipt7.total_amount:.2f}")
    print(f"   Verification: {receipt7.pre_vat_amount:.2f} + {receipt7.vat_amount:.2f} = {receipt7.pre_vat_amount + receipt7.vat_amount:.2f}")
    print(f"✅ Valid: {is_valid}")
    if warnings:
        print(f"⚠️  Warnings: {', '.join(warnings)}")
    else:
        print("✓ All checks passed!")
    
    # Summary
    print("\n\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Business number validation (Israeli check digit algorithm)")
    print("  ✓ Receipt date validation (7-year rule)")
    print("  ✓ Future date detection")
    print("  ✓ VAT calculation (17% Israeli rate)")
    print("  ✓ VAT verification with tolerance")
    print("  ✓ OCR confidence checking")
    print("  ✓ Missing field detection")
    print("  ✓ Hebrew error messages")
    print("  ✓ Automatic VAT recalculation")
    
    print("\nValidation Rules:")
    print("  • Business number must pass check digit test")
    print("  • Receipt date cannot be in the future")
    print("  • Receipt date cannot be older than 7 years")
    print("  • VAT calculation must match (within ±₪0.02)")
    print("  • OCR confidence must be ≥70% per field")
    print("  • Vendor name is required")
    print("  • Amount must be positive")
    print("  • Receipt date is required")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    demo_receipt_validation()
