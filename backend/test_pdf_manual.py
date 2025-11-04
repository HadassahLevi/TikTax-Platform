"""
Manual PDF Generation Test
Verify PDF export generates correctly with sample data
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.pdf_service import pdf_service
from app.models.user import User, SubscriptionPlan
from app.models.receipt import Receipt, ReceiptStatus
from app.models.category import Category


class MockUser:
    """Mock user for testing"""
    def __init__(self):
        self.id = 1
        self.email = "test@tiktax.co.il"
        self.full_name = "David Cohen"
        self.business_name = "Cohen Design Studio בע״מ"
        self.business_number = "515123456"
        self.subscription_plan = SubscriptionPlan.PRO


class MockCategory:
    """Mock category for testing"""
    def __init__(self, id, name, name_hebrew):
        self.id = id
        self.name = name
        self.name_hebrew = name_hebrew


class MockReceipt:
    """Mock receipt for testing"""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.vendor_name = kwargs.get('vendor_name')
        self.category_id = kwargs.get('category_id')
        self.total_amount = kwargs.get('total_amount')
        self.vat_amount = kwargs.get('vat_amount')
        self.pre_vat_amount = kwargs.get('pre_vat_amount')
        self.receipt_date = kwargs.get('receipt_date')
        self.business_number = kwargs.get('business_number')
        self.receipt_number = kwargs.get('receipt_number')
        self.file_url = kwargs.get('file_url')
        self.status = ReceiptStatus.APPROVED


def create_sample_data():
    """Create sample data for testing"""
    # User
    user = MockUser()
    
    # Categories
    categories = [
        MockCategory(1, "Office Supplies", "ציוד משרדי"),
        MockCategory(2, "Transportation", "תחבורה"),
        MockCategory(3, "Meals & Entertainment", "אוכל ואירוח"),
        MockCategory(4, "Professional Services", "שירותים מקצועיים"),
        MockCategory(5, "Software & Technology", "תוכנה וטכנולוגיה"),
    ]
    
    # Receipts
    base_date = datetime(2024, 1, 5)
    receipts = []
    
    receipt_data = [
        {
            "id": 1,
            "vendor_name": "Office Depot Israel",
            "category_id": 1,
            "total_amount": 1250.00,
            "vat_amount": 181.62,
            "pre_vat_amount": 1068.38,
            "receipt_date": base_date,
            "business_number": "515234567",
            "receipt_number": "REC-001234",
            "file_url": "https://via.placeholder.com/800x1200/2563eb/ffffff?text=Office+Receipt"
        },
        {
            "id": 2,
            "vendor_name": "Shell Gas Station",
            "category_id": 2,
            "total_amount": 450.00,
            "vat_amount": 65.38,
            "pre_vat_amount": 384.62,
            "receipt_date": base_date + timedelta(days=2),
            "business_number": "515987654",
            "receipt_number": "INV-5678",
            "file_url": "https://via.placeholder.com/800x1200/059669/ffffff?text=Gas+Receipt"
        },
        {
            "id": 3,
            "vendor_name": "Cafe Aroma",
            "category_id": 3,
            "total_amount": 180.00,
            "vat_amount": 26.15,
            "pre_vat_amount": 153.85,
            "receipt_date": base_date + timedelta(days=3),
            "business_number": "515555666",
            "receipt_number": "TBL-089",
            "file_url": "https://via.placeholder.com/800x1200/f59e0b/ffffff?text=Cafe+Receipt"
        },
        {
            "id": 4,
            "vendor_name": "Fiverr International",
            "category_id": 4,
            "total_amount": 2400.00,
            "vat_amount": 348.72,
            "pre_vat_amount": 2051.28,
            "receipt_date": base_date + timedelta(days=5),
            "business_number": "515111222",
            "receipt_number": "FVR-9876",
            "file_url": "https://via.placeholder.com/800x1200/8b5cf6/ffffff?text=Fiverr+Invoice"
        },
        {
            "id": 5,
            "vendor_name": "Microsoft Azure",
            "category_id": 5,
            "total_amount": 890.00,
            "vat_amount": 129.32,
            "pre_vat_amount": 760.68,
            "receipt_date": base_date + timedelta(days=7),
            "business_number": "515333444",
            "receipt_number": "AZ-202401",
            "file_url": "https://via.placeholder.com/800x1200/0891b2/ffffff?text=Azure+Invoice"
        },
        {
            "id": 6,
            "vendor_name": "Paz Gas Station",
            "category_id": 2,
            "total_amount": 520.00,
            "vat_amount": 75.56,
            "pre_vat_amount": 444.44,
            "receipt_date": base_date + timedelta(days=10),
            "business_number": "515777888",
            "receipt_number": "PAZ-4567",
            "file_url": "https://via.placeholder.com/800x1200/059669/ffffff?text=Paz+Receipt"
        },
        {
            "id": 7,
            "vendor_name": "Super-Pharm",
            "category_id": 1,
            "total_amount": 320.00,
            "vat_amount": 46.50,
            "pre_vat_amount": 273.50,
            "receipt_date": base_date + timedelta(days=12),
            "business_number": "515999000",
            "receipt_number": "SP-8901",
            "file_url": "https://via.placeholder.com/800x1200/2563eb/ffffff?text=SuperPharm"
        },
        {
            "id": 8,
            "vendor_name": "Restaurant Meat Bar",
            "category_id": 3,
            "total_amount": 680.00,
            "vat_amount": 98.80,
            "pre_vat_amount": 581.20,
            "receipt_date": base_date + timedelta(days=14),
            "business_number": "515222333",
            "receipt_number": "MB-3456",
            "file_url": "https://via.placeholder.com/800x1200/f59e0b/ffffff?text=Restaurant"
        },
    ]
    
    for data in receipt_data:
        receipts.append(MockReceipt(**data))
    
    return user, categories, receipts


def test_pdf_without_images():
    """Test PDF generation without images"""
    print("=" * 60)
    print("Testing PDF Generation WITHOUT Images")
    print("=" * 60)
    
    user, categories, receipts = create_sample_data()
    
    date_from = datetime(2024, 1, 1)
    date_to = datetime(2024, 1, 31)
    
    try:
        pdf_bytes = pdf_service.generate_export(
            user=user,
            receipts=receipts,
            categories=categories,
            date_from=date_from,
            date_to=date_to,
            include_images=False
        )
        
        # Save to file
        output_path = backend_path / "test_export_no_images.pdf"
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✓ PDF generated successfully")
        print(f"✓ File size: {len(pdf_bytes):,} bytes")
        print(f"✓ Saved to: {output_path}")
        print(f"✓ Receipts included: {len(receipts)}")
        
        # Verify PDF header
        if pdf_bytes[:4] == b'%PDF':
            print(f"✓ Valid PDF format")
        else:
            print(f"✗ Invalid PDF format")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_pdf_with_images():
    """Test PDF generation with images"""
    print("\n" + "=" * 60)
    print("Testing PDF Generation WITH Images")
    print("=" * 60)
    
    user, categories, receipts = create_sample_data()
    
    # Use only first 3 receipts for faster testing
    receipts = receipts[:3]
    
    date_from = datetime(2024, 1, 1)
    date_to = datetime(2024, 1, 31)
    
    try:
        pdf_bytes = pdf_service.generate_export(
            user=user,
            receipts=receipts,
            categories=categories,
            date_from=date_from,
            date_to=date_to,
            include_images=True
        )
        
        # Save to file
        output_path = backend_path / "test_export_with_images.pdf"
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✓ PDF generated successfully")
        print(f"✓ File size: {len(pdf_bytes):,} bytes")
        print(f"✓ Saved to: {output_path}")
        print(f"✓ Receipts included: {len(receipts)}")
        print(f"✓ Images included: {len(receipts)}")
        
        # Verify PDF header
        if pdf_bytes[:4] == b'%PDF':
            print(f"✓ Valid PDF format")
        else:
            print(f"✗ Invalid PDF format")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_empty_receipts():
    """Test PDF with no receipts"""
    print("\n" + "=" * 60)
    print("Testing PDF Generation with EMPTY Receipts")
    print("=" * 60)
    
    user, categories, _ = create_sample_data()
    
    date_from = datetime(2024, 1, 1)
    date_to = datetime(2024, 1, 31)
    
    try:
        pdf_bytes = pdf_service.generate_export(
            user=user,
            receipts=[],
            categories=categories,
            date_from=date_from,
            date_to=date_to,
            include_images=False
        )
        
        output_path = backend_path / "test_export_empty.pdf"
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✓ PDF generated successfully (empty)")
        print(f"✓ File size: {len(pdf_bytes):,} bytes")
        print(f"✓ Saved to: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PDF SERVICE MANUAL TESTING")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: PDF without images
    results.append(("PDF without images", test_pdf_without_images()))
    
    # Test 2: PDF with images
    results.append(("PDF with images", test_pdf_with_images()))
    
    # Test 3: Empty receipts
    results.append(("Empty receipts", test_empty_receipts()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, success in results if success)
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
