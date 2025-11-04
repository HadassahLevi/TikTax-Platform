"""
Integration tests for OCR and Receipt Processing Pipeline
Tests complete flow with sample Israeli receipts
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.ocr_service import ocr_service
from app.services.receipt_service import receipt_service
from app.models.receipt import Receipt, ReceiptStatus
from app.models.category import Category


class TestOCRIntegration:
    """Integration tests for complete receipt processing pipeline"""
    
    @pytest.fixture
    def db_session(self):
        """Mock database session"""
        session = Mock(spec=Session)
        session.query.return_value.filter.return_value.first.return_value = None
        return session
    
    @pytest.mark.asyncio
    async def test_full_pipeline_hebrew_receipt(self, db_session):
        """Test complete processing with real Hebrew receipt text"""
        # Sample Hebrew receipt from Israeli supermarket
        sample_receipt_text = """
        שופרסל דיל
        ירושלים 123, תל אביב
        ח.פ: 500123456
        קבלה מס': 78945
        תאריך: 01/11/2024 שעה: 14:23
        
        פריטים:
        חלב תנובה 3% - 6.50
        לחם שחור - 8.90
        גבינה צהובה - 24.90
        עגבניות (ק"ג) - 12.80
        
        סה"כ לפני מע"מ: 45.73
        מע"מ (17%): 7.77
        סה"כ לתשלום: ₪53.50
        
        תודה על הקנייה!
        עוסק מורשה 500123456
        """
        
        # Create receipt object
        receipt = Receipt(
            id=1,
            user_id=100,
            original_filename="supermarket_receipt.jpg",
            file_url="https://s3.example.com/receipts/test1.jpg",
            file_size=150000,
            mime_type="image/jpeg",
            status=ReceiptStatus.PROCESSING
        )
        
        # Mock database query to return our receipt
        db_session.query.return_value.filter.return_value.first.return_value = receipt
        
        # Mock food category
        food_category = Category(id=1, name_hebrew="מזון ושתייה", name_english="Food & Beverages")
        
        # Setup mock to return category when queried
        def mock_category_query(*args, **kwargs):
            mock = Mock()
            mock.filter.return_value.first.return_value = food_category
            return mock
        
        db_session.query.side_effect = lambda model: (
            mock_category_query() if model == Category 
            else Mock(filter=lambda *a, **k: Mock(first=lambda: receipt))
        )
        
        # Mock Vision API response
        mock_vision_response = Mock()
        mock_vision_response.error.message = ""
        mock_vision_response.full_text_annotation.text = sample_receipt_text
        mock_vision_response.full_text_annotation.pages = [Mock()]
        
        with patch('app.services.ocr_service.vision.ImageAnnotatorClient') as mock_client:
            with patch('app.services.ocr_service.service_account.Credentials.from_service_account_file'):
                with patch('requests.get') as mock_get:
                    # Setup mocks
                    mock_get.return_value.content = b"fake_image_data"
                    mock_get.return_value.raise_for_status = Mock()
                    
                    mock_instance = mock_client.return_value
                    mock_instance.document_text_detection = Mock(return_value=mock_vision_response)
                    
                    # Process receipt
                    await receipt_service.process_receipt(1, db_session)
        
        # Assertions
        assert receipt.status == ReceiptStatus.REVIEW
        assert receipt.vendor_name == "שופרסל דיל"
        assert receipt.business_number == "500123456"
        assert receipt.receipt_number == "78945"
        assert receipt.receipt_date.strftime("%Y-%m-%d") == "2024-11-01"
        assert receipt.total_amount == 53.50
        assert receipt.vat_amount == 7.77
        assert abs(receipt.pre_vat_amount - 45.73) < 0.01
        assert receipt.category_id == 1  # Auto-categorized to food
        assert receipt.confidence_score > 0.5
        assert receipt.processing_completed_at is not None
    
    @pytest.mark.asyncio
    async def test_full_pipeline_gas_station_receipt(self, db_session):
        """Test processing gas station receipt"""
        gas_receipt_text = """
        PAZ - תדלוק עצמי
        תחנת דלק - נתניה
        עוסק מורשה: 520147852
        
        חשבונית מס': 456123
        תאריך: 03.11.2024
        שעה: 08:15
        
        דלק 95 - 45.2 ליטר
        מחיר ליטר: 7.15
        
        סה"כ: ₪323.18
        כולל מע"מ: ₪46.51
        """
        
        receipt = Receipt(
            id=2,
            user_id=100,
            file_url="https://s3.example.com/receipts/gas.jpg",
            original_filename="gas_receipt.jpg",
            file_size=100000,
            mime_type="image/jpeg",
            status=ReceiptStatus.PROCESSING
        )
        
        db_session.query.return_value.filter.return_value.first.return_value = receipt
        
        # Mock transportation category
        transport_category = Category(id=2, name_hebrew="תחבורה", name_english="Transportation")
        
        def mock_query(*args, **kwargs):
            mock = Mock()
            mock.filter.return_value.first.return_value = transport_category
            return mock
        
        db_session.query.side_effect = lambda model: (
            mock_query() if model == Category 
            else Mock(filter=lambda *a, **k: Mock(first=lambda: receipt))
        )
        
        mock_vision_response = Mock()
        mock_vision_response.error.message = ""
        mock_vision_response.full_text_annotation.text = gas_receipt_text
        mock_vision_response.full_text_annotation.pages = [Mock()]
        
        with patch('app.services.ocr_service.vision.ImageAnnotatorClient') as mock_client:
            with patch('app.services.ocr_service.service_account.Credentials.from_service_account_file'):
                with patch('requests.get') as mock_get:
                    mock_get.return_value.content = b"fake_image_data"
                    mock_get.return_value.raise_for_status = Mock()
                    
                    mock_instance = mock_client.return_value
                    mock_instance.document_text_detection = Mock(return_value=mock_vision_response)
                    
                    await receipt_service.process_receipt(2, db_session)
        
        # Assertions
        assert receipt.status == ReceiptStatus.REVIEW
        assert "PAZ" in receipt.vendor_name or "תדלוק" in receipt.vendor_name
        assert receipt.business_number == "520147852"
        assert receipt.total_amount == 323.18
        assert receipt.vat_amount == 46.51
        assert receipt.category_id == 2  # Auto-categorized to transportation
    
    @pytest.mark.asyncio
    async def test_duplicate_detection_integration(self, db_session):
        """Test duplicate detection in full pipeline"""
        receipt_text = """
        קפה קפה
        ח.פ: 510258963
        קבלה: 789
        01/11/2024
        סה"כ: ₪85.00
        """
        
        # Create new receipt
        new_receipt = Receipt(
            id=10,
            user_id=100,
            file_url="https://s3.example.com/receipts/new.jpg",
            original_filename="new.jpg",
            file_size=50000,
            mime_type="image/jpeg",
            status=ReceiptStatus.PROCESSING
        )
        
        # Existing similar receipt
        existing_receipt = Receipt(
            id=5,
            user_id=100,
            vendor_name="קפה קפה",
            receipt_date=datetime(2024, 11, 1, 10, 0),
            total_amount=85.00,
            status=ReceiptStatus.APPROVED
        )
        
        # Mock queries
        def mock_receipt_query(*args, **kwargs):
            class MockQuery:
                def filter(self, *args, **kwargs):
                    return self
                
                def first(self):
                    # Return new receipt on first call, existing on duplicate check
                    if not hasattr(self, '_called'):
                        self._called = True
                        return new_receipt
                    return existing_receipt
            
            return MockQuery()
        
        db_session.query.side_effect = lambda model: (
            Mock(filter=lambda *a, **k: Mock(first=lambda: None)) if model == Category
            else mock_receipt_query()
        )
        
        mock_vision_response = Mock()
        mock_vision_response.error.message = ""
        mock_vision_response.full_text_annotation.text = receipt_text
        mock_vision_response.full_text_annotation.pages = [Mock()]
        
        with patch('app.services.ocr_service.vision.ImageAnnotatorClient') as mock_client:
            with patch('app.services.ocr_service.service_account.Credentials.from_service_account_file'):
                with patch('requests.get') as mock_get:
                    mock_get.return_value.content = b"fake_image_data"
                    mock_get.return_value.raise_for_status = Mock()
                    
                    mock_instance = mock_client.return_value
                    mock_instance.document_text_detection = Mock(return_value=mock_vision_response)
                    
                    await receipt_service.process_receipt(10, db_session)
        
        # Should be marked as duplicate
        assert new_receipt.status == ReceiptStatus.DUPLICATE
        assert new_receipt.is_duplicate is True
        assert new_receipt.duplicate_of_id == 5
    
    @pytest.mark.asyncio
    async def test_low_confidence_receipt(self, db_session):
        """Test handling of poor quality receipt with low confidence"""
        poor_quality_text = """
        Sme Sh0p
        12 456 89
        
        T0tal: 5O.OO
        """
        
        receipt = Receipt(
            id=20,
            user_id=100,
            file_url="https://s3.example.com/receipts/blurry.jpg",
            original_filename="blurry.jpg",
            file_size=30000,
            mime_type="image/jpeg",
            status=ReceiptStatus.PROCESSING
        )
        
        db_session.query.return_value.filter.return_value.first.return_value = receipt
        
        mock_vision_response = Mock()
        mock_vision_response.error.message = ""
        mock_vision_response.full_text_annotation.text = poor_quality_text
        mock_vision_response.full_text_annotation.pages = [Mock()]
        
        with patch('app.services.ocr_service.vision.ImageAnnotatorClient') as mock_client:
            with patch('app.services.ocr_service.service_account.Credentials.from_service_account_file'):
                with patch('requests.get') as mock_get:
                    mock_get.return_value.content = b"fake_image_data"
                    mock_get.return_value.raise_for_status = Mock()
                    
                    mock_instance = mock_client.return_value
                    mock_instance.document_text_detection = Mock(return_value=mock_vision_response)
                    
                    await receipt_service.process_receipt(20, db_session)
        
        # Should still process but with low confidence
        assert receipt.status == ReceiptStatus.REVIEW
        assert receipt.confidence_score < 0.7  # Low confidence expected
    
    def test_hebrew_encoding_handling(self):
        """Test proper Hebrew text encoding"""
        hebrew_text = "קבלה מס' 123 - סה״כ: ₪100.00"
        
        # Should not raise encoding errors
        parsed = ocr_service._parse_receipt_text(hebrew_text)
        
        assert parsed is not None
        assert isinstance(parsed, dict)
    
    def test_mixed_rtl_ltr_text(self):
        """Test handling of mixed RTL (Hebrew) and LTR (English/numbers) text"""
        mixed_text = """
        Cafe123 קפה
        Receipt מס': 456
        Total סה"כ: 50.00₪
        """
        
        parsed = ocr_service._parse_receipt_text(mixed_text)
        
        assert parsed["receipt_number"] == "456"
        assert parsed["total_amount"] == 50.00
