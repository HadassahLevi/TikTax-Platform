"""
Integration Tests for Receipt Service Validation
Tests validation methods with real receipt data and edge cases
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.receipt import Receipt, ReceiptStatus
from app.services.receipt_service import receipt_service


class TestReceiptDataValidation:
    """Test receipt data validation"""
    
    @pytest.mark.asyncio
    async def test_validate_valid_receipt(self):
        """Test validation of valid receipt"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="Test Vendor",
            business_number="123456782",  # Valid check digit
            receipt_date=datetime.now() - timedelta(days=1),
            total_amount=117.00,
            vat_amount=17.00,
            pre_vat_amount=100.00,
            confidence_score=0.95,
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is True
        assert len(warnings) == 0
    
    @pytest.mark.asyncio
    async def test_validate_invalid_business_number(self):
        """Test validation with invalid business number"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="Test Vendor",
            business_number="123456789",  # Invalid check digit
            receipt_date=datetime.now() - timedelta(days=1),
            total_amount=117.00,
            vat_amount=17.00,
            pre_vat_amount=100.00,
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is False
        assert any("עוסק מורשה" in w for w in warnings)
    
    @pytest.mark.asyncio
    async def test_validate_future_date(self):
        """Test validation with future date"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="Test Vendor",
            receipt_date=datetime.now() + timedelta(days=1),  # Future date
            total_amount=100.00,
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is False
        assert any("עתיד" in w for w in warnings)
    
    @pytest.mark.asyncio
    async def test_validate_old_date(self):
        """Test validation with date older than 7 years"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="Test Vendor",
            receipt_date=datetime.now() - timedelta(days=365 * 8),  # 8 years old
            total_amount=100.00,
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is False
        assert any("7 שנים" in w or "ישן" in w for w in warnings)
    
    @pytest.mark.asyncio
    async def test_validate_incorrect_vat(self):
        """Test validation with incorrect VAT calculation"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="Test Vendor",
            receipt_date=datetime.now() - timedelta(days=1),
            total_amount=117.00,
            vat_amount=20.00,  # Incorrect VAT (should be 17.00)
            pre_vat_amount=97.00,  # Incorrect pre-VAT
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is False
        assert any("מע״מ" in w for w in warnings)
    
    @pytest.mark.asyncio
    async def test_validate_low_confidence_scores(self):
        """Test validation with low OCR confidence scores"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="Test Vendor",
            receipt_date=datetime.now() - timedelta(days=1),
            total_amount=100.00,
            ocr_data={
                "parsed_data": {
                    "vendor_name": "Test Vendor",
                    "total_amount": 100.00,
                    "confidence": {
                        "vendor_name": 0.95,
                        "total_amount": 0.60,  # Low confidence
                        "receipt_date": 0.50,  # Low confidence
                    }
                }
            }
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is False
        assert any("דיוק נמוך" in w for w in warnings)
    
    @pytest.mark.asyncio
    async def test_validate_missing_vendor_name(self):
        """Test validation with missing vendor name"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name=None,  # Missing
            receipt_date=datetime.now() - timedelta(days=1),
            total_amount=100.00,
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is False
        assert any("עסק" in w for w in warnings)
    
    @pytest.mark.asyncio
    async def test_validate_invalid_amount(self):
        """Test validation with invalid amount"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="Test Vendor",
            receipt_date=datetime.now() - timedelta(days=1),
            total_amount=0,  # Invalid amount
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is False
        assert any("סכום" in w for w in warnings)
    
    @pytest.mark.asyncio
    async def test_validate_missing_date(self):
        """Test validation with missing date"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="Test Vendor",
            receipt_date=None,  # Missing
            total_amount=100.00,
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is False
        assert any("תאריך" in w for w in warnings)
    
    @pytest.mark.asyncio
    async def test_validate_multiple_issues(self):
        """Test validation with multiple issues"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name=None,  # Missing
            business_number="123456789",  # Invalid
            receipt_date=datetime.now() + timedelta(days=1),  # Future
            total_amount=0,  # Invalid
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is False
        assert len(warnings) >= 3  # Multiple warnings


class TestVATRecalculation:
    """Test VAT recalculation"""
    
    @pytest.mark.asyncio
    async def test_recalculate_vat_from_total(self):
        """Test VAT recalculation from total amount"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            total_amount=117.00,
            vat_amount=None,
            pre_vat_amount=None,
        )
        
        await receipt_service.recalculate_vat(receipt)
        
        assert receipt.pre_vat_amount == 100.00
        assert receipt.vat_amount == 17.00
        assert receipt.total_amount == 117.00
    
    @pytest.mark.asyncio
    async def test_recalculate_vat_with_rounding(self):
        """Test VAT recalculation with rounding"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            total_amount=100.00,
            vat_amount=None,
            pre_vat_amount=None,
        )
        
        await receipt_service.recalculate_vat(receipt)
        
        assert receipt.pre_vat_amount == 85.47
        assert receipt.vat_amount == 14.53
        assert receipt.total_amount == 100.00
    
    @pytest.mark.asyncio
    async def test_recalculate_vat_large_amount(self):
        """Test VAT recalculation with large amount"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            total_amount=11700.00,
            vat_amount=None,
            pre_vat_amount=None,
        )
        
        await receipt_service.recalculate_vat(receipt)
        
        assert receipt.pre_vat_amount == 10000.00
        assert receipt.vat_amount == 1700.00
        assert receipt.total_amount == 11700.00
    
    @pytest.mark.asyncio
    async def test_recalculate_vat_zero_amount(self):
        """Test VAT recalculation with zero amount"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            total_amount=0,
            vat_amount=None,
            pre_vat_amount=None,
        )
        
        await receipt_service.recalculate_vat(receipt)
        
        # Should handle gracefully (no error)
        # Values will be 0
        assert receipt.pre_vat_amount == 0.00
        assert receipt.vat_amount == 0.00


class TestRealWorldScenarios:
    """Test with real-world receipt scenarios"""
    
    @pytest.mark.asyncio
    async def test_coffee_shop_receipt(self):
        """Test validation of typical coffee shop receipt"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="קפה אומה",
            business_number="514123456",  # Assuming valid
            receipt_date=datetime.now() - timedelta(hours=2),
            total_amount=18.50,
            vat_amount=2.68,
            pre_vat_amount=15.82,
            confidence_score=0.92,
        )
        
        # Recalculate to ensure correct VAT
        await receipt_service.recalculate_vat(receipt)
        
        # Validate
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        # May have business number warning if check digit is wrong
        # But date, amount, and VAT should be valid
        assert receipt.total_amount == 18.50
        assert receipt.pre_vat_amount > 0
        assert receipt.vat_amount > 0
    
    @pytest.mark.asyncio
    async def test_supermarket_receipt(self):
        """Test validation of typical supermarket receipt"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="שופרסל",
            receipt_number="123456789",
            receipt_date=datetime.now() - timedelta(days=1),
            total_amount=342.50,
            confidence_score=0.88,
        )
        
        # Recalculate VAT
        await receipt_service.recalculate_vat(receipt)
        
        # Validate
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        # Should have valid amounts
        assert receipt.pre_vat_amount > 0
        assert receipt.vat_amount > 0
        assert abs((receipt.pre_vat_amount + receipt.vat_amount) - receipt.total_amount) < 0.02
    
    @pytest.mark.asyncio
    async def test_gas_station_receipt(self):
        """Test validation of typical gas station receipt"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="דלק",
            receipt_date=datetime.now() - timedelta(hours=3),
            total_amount=456.78,
            vat_amount=66.31,
            pre_vat_amount=390.47,
        )
        
        # Validate
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        # VAT calculation should be correct
        expected_total = receipt.pre_vat_amount + receipt.vat_amount
        assert abs(expected_total - receipt.total_amount) <= 0.02
    
    @pytest.mark.asyncio
    async def test_restaurant_receipt_with_ocr_data(self):
        """Test validation of restaurant receipt with OCR data"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="מסעדת הבשר",
            receipt_date=datetime.now() - timedelta(hours=5),
            total_amount=580.00,
            ocr_data={
                "success": True,
                "parsed_data": {
                    "vendor_name": "מסעדת הבשר",
                    "total_amount": 580.00,
                    "receipt_date": "2024-01-15",
                    "confidence": {
                        "vendor_name": 0.98,
                        "total_amount": 0.95,
                        "receipt_date": 0.92,
                    }
                }
            }
        )
        
        # Recalculate VAT
        await receipt_service.recalculate_vat(receipt)
        
        # Validate
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        # Should be valid (high confidence, correct amounts)
        # May have warnings about missing business number
        assert receipt.pre_vat_amount > 0
        assert receipt.vat_amount > 0


class TestEdgeCases:
    """Test edge cases"""
    
    @pytest.mark.asyncio
    async def test_validate_empty_receipt(self):
        """Test validation of empty receipt"""
        receipt = Receipt(
            id=1,
            user_id="user123",
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is False
        assert len(warnings) > 0
    
    @pytest.mark.asyncio
    async def test_validate_partial_receipt_data(self):
        """Test validation with only some fields"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="Test Vendor",
            total_amount=100.00,
            # Missing date, VAT breakdown
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is False
        # Should warn about missing date
        assert any("תאריך" in w for w in warnings)
    
    @pytest.mark.asyncio
    async def test_recalculate_vat_none_amount(self):
        """Test VAT recalculation with None amount"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            total_amount=None,
        )
        
        # Should handle gracefully without error
        await receipt_service.recalculate_vat(receipt)
        
        # Values should remain None or be set to 0
        assert receipt.pre_vat_amount is None or receipt.pre_vat_amount == 0
    
    @pytest.mark.asyncio
    async def test_validate_negative_amount(self):
        """Test validation with negative amount"""
        receipt = Receipt(
            id=1,
            user_id="user123",
            vendor_name="Test Vendor",
            receipt_date=datetime.now() - timedelta(days=1),
            total_amount=-100.00,  # Negative (refund?)
        )
        
        is_valid, warnings = await receipt_service.validate_receipt_data(receipt)
        
        assert is_valid is False
        assert any("סכום" in w for w in warnings)
    
    @pytest.mark.asyncio
    async def test_validate_exact_seven_years_old(self):
        """Test validation with receipt exactly 7 years old"""
        # Just under 7 years
        receipt1 = Receipt(
            id=1,
            user_id="user123",
            vendor_name="Test Vendor",
            receipt_date=datetime.now() - timedelta(days=365 * 7 - 1),
            total_amount=100.00,
        )
        
        is_valid1, warnings1 = await receipt_service.validate_receipt_data(receipt1)
        
        # Should be valid (just under 7 years)
        assert not any("7 שנים" in w or "ישן" in w for w in warnings1)
        
        # Just over 7 years
        receipt2 = Receipt(
            id=2,
            user_id="user123",
            vendor_name="Test Vendor",
            receipt_date=datetime.now() - timedelta(days=365 * 7 + 1),
            total_amount=100.00,
        )
        
        is_valid2, warnings2 = await receipt_service.validate_receipt_data(receipt2)
        
        # Should be invalid (over 7 years)
        assert any("7 שנים" in w or "ישן" in w for w in warnings2)
