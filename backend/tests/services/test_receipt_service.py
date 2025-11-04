"""
Unit tests for Receipt Service
Tests processing pipeline, categorization, and duplicate detection
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.services.receipt_service import ReceiptService
from app.models.receipt import Receipt, ReceiptStatus
from app.models.category import Category
from app.models.user import User


class TestReceiptService:
    """Test receipt service processing pipeline"""
    
    @pytest.fixture
    def db_session(self):
        """Mock database session"""
        return Mock(spec=Session)
    
    @pytest.fixture
    def receipt_service(self):
        """Create receipt service instance"""
        return ReceiptService()
    
    @pytest.fixture
    def sample_receipt(self):
        """Create sample receipt object"""
        receipt = Receipt(
            id=1,
            user_id=100,
            original_filename="receipt.jpg",
            file_url="https://s3.example.com/receipt.jpg",
            file_size=50000,
            mime_type="image/jpeg",
            status=ReceiptStatus.PROCESSING
        )
        return receipt
    
    @pytest.mark.asyncio
    async def test_process_receipt_success(self, receipt_service, db_session, sample_receipt):
        """Test successful receipt processing"""
        # Mock database query
        db_session.query.return_value.filter.return_value.first.return_value = sample_receipt
        
        # Mock OCR result
        mock_ocr_result = {
            "success": True,
            "full_text": "Test receipt",
            "parsed_data": {
                "vendor_name": "Test Vendor",
                "business_number": "123456789",
                "receipt_number": "001",
                "receipt_date": "2024-11-01",
                "total_amount": 100.00,
                "vat_amount": 17.00,
                "pre_vat_amount": 83.00,
                "confidence": {
                    "vendor_name": 0.90,
                    "business_number": 0.85,
                    "receipt_number": 0.80,
                    "receipt_date": 0.75,
                    "total_amount": 0.95,
                    "vat_amount": 0.88
                }
            },
            "raw_response": {}
        }
        
        with patch('app.services.receipt_service.ocr_service.retry_extraction', new=AsyncMock(return_value=mock_ocr_result)):
            with patch.object(receipt_service, '_categorize_receipt', new=AsyncMock(return_value=5)):
                with patch.object(receipt_service, '_check_duplicate', new=AsyncMock(return_value=False)):
                    await receipt_service.process_receipt(1, db_session)
        
        # Assertions
        assert sample_receipt.status == ReceiptStatus.REVIEW
        assert sample_receipt.vendor_name == "Test Vendor"
        assert sample_receipt.business_number == "123456789"
        assert sample_receipt.total_amount == 100.00
        assert sample_receipt.vat_amount == 17.00
        assert sample_receipt.confidence_score > 0
        assert sample_receipt.category_id == 5
        assert sample_receipt.processing_completed_at is not None
        assert db_session.commit.called
    
    @pytest.mark.asyncio
    async def test_process_receipt_ocr_failure(self, receipt_service, db_session, sample_receipt):
        """Test receipt processing with OCR failure"""
        db_session.query.return_value.filter.return_value.first.return_value = sample_receipt
        
        mock_ocr_result = {
            "success": False,
            "error": "OCR failed",
            "full_text": "",
            "parsed_data": {}
        }
        
        with patch('app.services.receipt_service.ocr_service.retry_extraction', new=AsyncMock(return_value=mock_ocr_result)):
            await receipt_service.process_receipt(1, db_session)
        
        assert sample_receipt.status == ReceiptStatus.FAILED
        assert sample_receipt.processing_completed_at is not None
        assert db_session.commit.called
    
    @pytest.mark.asyncio
    async def test_process_receipt_duplicate_detected(self, receipt_service, db_session, sample_receipt):
        """Test receipt processing with duplicate detection"""
        db_session.query.return_value.filter.return_value.first.return_value = sample_receipt
        
        mock_ocr_result = {
            "success": True,
            "full_text": "Test",
            "parsed_data": {
                "vendor_name": "Vendor",
                "total_amount": 50.00,
                "receipt_date": "2024-11-01",
                "confidence": {}
            }
        }
        
        with patch('app.services.receipt_service.ocr_service.retry_extraction', new=AsyncMock(return_value=mock_ocr_result)):
            with patch.object(receipt_service, '_categorize_receipt', new=AsyncMock(return_value=None)):
                with patch.object(receipt_service, '_check_duplicate', new=AsyncMock(return_value=True)):
                    await receipt_service.process_receipt(1, db_session)
        
        assert sample_receipt.status == ReceiptStatus.DUPLICATE
        assert sample_receipt.is_duplicate is True
    
    @pytest.mark.asyncio
    async def test_categorize_receipt_hebrew_keywords(self, receipt_service, db_session):
        """Test auto-categorization with Hebrew keywords"""
        receipt = Receipt(vendor_name="מסעדת השף")
        
        # Mock category query
        mock_category = Category(id=10, name_hebrew="מזון ושתייה")
        db_session.query.return_value.filter.return_value.first.return_value = mock_category
        
        category_id = await receipt_service._categorize_receipt(receipt, db_session)
        
        assert category_id == 10
    
    @pytest.mark.asyncio
    async def test_categorize_receipt_english_keywords(self, receipt_service, db_session):
        """Test auto-categorization with English keywords"""
        receipt = Receipt(vendor_name="PAZ Gas Station")
        
        mock_category = Category(id=3, name_hebrew="תחבורה")
        db_session.query.return_value.filter.return_value.first.return_value = mock_category
        
        category_id = await receipt_service._categorize_receipt(receipt, db_session)
        
        assert category_id == 3
    
    @pytest.mark.asyncio
    async def test_categorize_receipt_no_match(self, receipt_service, db_session):
        """Test categorization with no keyword match"""
        receipt = Receipt(vendor_name="Unknown Vendor XYZ")
        
        category_id = await receipt_service._categorize_receipt(receipt, db_session)
        
        assert category_id is None
    
    @pytest.mark.asyncio
    async def test_categorize_receipt_no_vendor_name(self, receipt_service, db_session):
        """Test categorization with missing vendor name"""
        receipt = Receipt(vendor_name=None)
        
        category_id = await receipt_service._categorize_receipt(receipt, db_session)
        
        assert category_id is None
    
    @pytest.mark.asyncio
    async def test_check_duplicate_exact_match(self, receipt_service, db_session):
        """Test duplicate detection with exact match"""
        receipt = Receipt(
            id=1,
            user_id=100,
            vendor_name="Test Vendor",
            receipt_date=datetime(2024, 11, 1),
            total_amount=100.00
        )
        
        # Mock existing receipt
        existing_receipt = Receipt(
            id=2,
            user_id=100,
            vendor_name="Test Vendor",
            receipt_date=datetime(2024, 11, 1),
            total_amount=100.00,
            status=ReceiptStatus.APPROVED
        )
        
        db_session.query.return_value.filter.return_value.first.return_value = existing_receipt
        
        is_duplicate = await receipt_service._check_duplicate(receipt, db_session)
        
        assert is_duplicate is True
        assert receipt.duplicate_of_id == 2
    
    @pytest.mark.asyncio
    async def test_check_duplicate_within_tolerance(self, receipt_service, db_session):
        """Test duplicate detection with amount tolerance"""
        receipt = Receipt(
            id=1,
            user_id=100,
            vendor_name="Cafe",
            receipt_date=datetime(2024, 11, 1),
            total_amount=100.00
        )
        
        # Similar receipt with 3% difference (within 5% tolerance)
        existing_receipt = Receipt(
            id=2,
            user_id=100,
            vendor_name="Cafe",
            receipt_date=datetime(2024, 11, 1, 12, 0),  # Same day, different time
            total_amount=103.00,
            status=ReceiptStatus.REVIEW
        )
        
        db_session.query.return_value.filter.return_value.first.return_value = existing_receipt
        
        is_duplicate = await receipt_service._check_duplicate(receipt, db_session)
        
        assert is_duplicate is True
    
    @pytest.mark.asyncio
    async def test_check_duplicate_different_date(self, receipt_service, db_session):
        """Test no duplicate when dates differ by more than 1 day"""
        receipt = Receipt(
            id=1,
            user_id=100,
            vendor_name="Shop",
            receipt_date=datetime(2024, 11, 1),
            total_amount=50.00
        )
        
        db_session.query.return_value.filter.return_value.first.return_value = None
        
        is_duplicate = await receipt_service._check_duplicate(receipt, db_session)
        
        assert is_duplicate is False
    
    @pytest.mark.asyncio
    async def test_check_duplicate_different_amount(self, receipt_service, db_session):
        """Test no duplicate when amounts differ significantly"""
        receipt = Receipt(
            id=1,
            user_id=100,
            vendor_name="Store",
            receipt_date=datetime(2024, 11, 1),
            total_amount=100.00
        )
        
        # Amount differs by more than 5%
        db_session.query.return_value.filter.return_value.first.return_value = None
        
        is_duplicate = await receipt_service._check_duplicate(receipt, db_session)
        
        assert is_duplicate is False
    
    @pytest.mark.asyncio
    async def test_check_duplicate_missing_data(self, receipt_service, db_session):
        """Test duplicate check skipped when required data missing"""
        receipt = Receipt(
            id=1,
            user_id=100,
            vendor_name=None,  # Missing vendor
            receipt_date=datetime(2024, 11, 1),
            total_amount=100.00
        )
        
        is_duplicate = await receipt_service._check_duplicate(receipt, db_session)
        
        assert is_duplicate is False
    
    @pytest.mark.asyncio
    async def test_process_receipt_not_found(self, receipt_service, db_session):
        """Test processing with non-existent receipt"""
        db_session.query.return_value.filter.return_value.first.return_value = None
        
        # Should not raise exception
        await receipt_service.process_receipt(999, db_session)
        
        # Should not commit if receipt not found
        assert not db_session.commit.called
    
    @pytest.mark.asyncio
    async def test_process_receipt_exception_handling(self, receipt_service, db_session, sample_receipt):
        """Test exception handling during processing"""
        db_session.query.return_value.filter.return_value.first.return_value = sample_receipt
        
        # Mock OCR to raise exception
        with patch('app.services.receipt_service.ocr_service.retry_extraction', new=AsyncMock(side_effect=Exception("Unexpected error"))):
            await receipt_service.process_receipt(1, db_session)
        
        assert sample_receipt.status == ReceiptStatus.FAILED
        assert sample_receipt.processing_completed_at is not None
    
    @pytest.mark.asyncio
    async def test_confidence_score_calculation(self, receipt_service, db_session, sample_receipt):
        """Test confidence score averaging"""
        db_session.query.return_value.filter.return_value.first.return_value = sample_receipt
        
        mock_ocr_result = {
            "success": True,
            "full_text": "Test",
            "parsed_data": {
                "confidence": {
                    "vendor_name": 0.90,
                    "business_number": 0.80,
                    "total_amount": 1.0
                }
            }
        }
        
        with patch('app.services.receipt_service.ocr_service.retry_extraction', new=AsyncMock(return_value=mock_ocr_result)):
            with patch.object(receipt_service, '_categorize_receipt', new=AsyncMock(return_value=None)):
                with patch.object(receipt_service, '_check_duplicate', new=AsyncMock(return_value=False)):
                    await receipt_service.process_receipt(1, db_session)
        
        # Average: (0.90 + 0.80 + 1.0) / 3 = 0.90
        assert abs(sample_receipt.confidence_score - 0.90) < 0.01
