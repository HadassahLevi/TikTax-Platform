"""
Unit tests for OCR Service
Tests Hebrew text parsing, field extraction, and confidence scoring
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.ocr_service import OCRService


class TestOCRService:
    """Test OCR service functionality"""
    
    @pytest.fixture
    def ocr_service(self):
        """Create OCR service instance with mocked Vision client"""
        with patch('app.services.ocr_service.service_account.Credentials.from_service_account_file'):
            with patch('app.services.ocr_service.vision.ImageAnnotatorClient'):
                service = OCRService()
                return service
    
    def test_parse_receipt_text_full_hebrew(self, ocr_service):
        """Test parsing complete Hebrew receipt"""
        receipt_text = """
        סופר פארם בע״מ
        ח.פ: 123456789
        קבלה מספר: 45678
        תאריך: 15/10/2024
        
        פריטים:
        חלב 3% - 6.50
        לחם - 8.90
        גבינה - 25.00
        
        סה"כ לפני מע"מ: 34.53
        מע"מ: 5.87
        סה"כ לתשלום: ₪40.40
        
        תודה ושוב!
        """
        
        parsed = ocr_service._parse_receipt_text(receipt_text)
        
        # Assertions
        assert parsed["vendor_name"] == "סופר פארם בע״מ"
        assert parsed["business_number"] == "123456789"
        assert parsed["receipt_number"] == "45678"
        assert parsed["receipt_date"] == "2024-10-15"
        assert parsed["total_amount"] == 40.40
        assert parsed["vat_amount"] == 5.87
        assert parsed["pre_vat_amount"] == 34.53
        
        # Check confidence scores
        assert parsed["confidence"]["vendor_name"] > 0
        assert parsed["confidence"]["business_number"] > 0
        assert parsed["confidence"]["total_amount"] > 0
    
    def test_parse_receipt_text_english(self, ocr_service):
        """Test parsing English receipt"""
        receipt_text = """
        Cafe Cafe Ltd.
        Business No: 987654321
        Receipt #: 12345
        Date: 20/11/2024
        
        Total: 125.50
        VAT: 21.33
        """
        
        parsed = ocr_service._parse_receipt_text(receipt_text)
        
        assert parsed["vendor_name"] == "Cafe Cafe Ltd."
        assert parsed["business_number"] == "987654321"
        assert parsed["receipt_number"] == "12345"
        assert parsed["receipt_date"] == "2024-11-20"
        assert parsed["total_amount"] == 125.50
        assert parsed["vat_amount"] == 21.33
    
    def test_parse_receipt_text_mixed_hebrew_english(self, ocr_service):
        """Test parsing mixed Hebrew-English receipt"""
        receipt_text = """
        Pizza Hut ישראל
        עוסק מורשה: 555444333
        חשבונית: 9999
        15.09.2024
        
        Total: ₪89.90
        מע"מ: ₪13.00
        """
        
        parsed = ocr_service._parse_receipt_text(receipt_text)
        
        assert "Pizza Hut" in parsed["vendor_name"]
        assert parsed["business_number"] == "555444333"
        assert parsed["receipt_number"] == "9999"
        assert parsed["total_amount"] == 89.90
        assert parsed["vat_amount"] == 13.00
    
    def test_parse_receipt_with_vat_calculation(self, ocr_service):
        """Test automatic VAT calculation when only total is present"""
        receipt_text = """
        קפה נמרוד
        ח.פ: 111222333
        
        סה"כ: 100.00
        """
        
        parsed = ocr_service._parse_receipt_text(receipt_text)
        
        assert parsed["total_amount"] == 100.00
        # VAT should be calculated (17%)
        assert parsed["vat_amount"] is not None
        assert abs(parsed["vat_amount"] - 14.53) < 0.01  # 100 * 0.17 / 1.17
        assert parsed["pre_vat_amount"] is not None
        assert abs(parsed["pre_vat_amount"] - 85.47) < 0.01
    
    def test_parse_receipt_partial_data(self, ocr_service):
        """Test parsing receipt with missing fields"""
        receipt_text = """
        חנות ABC
        
        סה"כ: 50.00
        """
        
        parsed = ocr_service._parse_receipt_text(receipt_text)
        
        assert parsed["vendor_name"] == "חנות ABC"
        assert parsed["business_number"] is None
        assert parsed["receipt_number"] is None
        assert parsed["receipt_date"] is None
        assert parsed["total_amount"] == 50.00
    
    def test_parse_receipt_no_data(self, ocr_service):
        """Test parsing empty or invalid text"""
        parsed = ocr_service._parse_receipt_text("")
        
        assert parsed["vendor_name"] is None
        assert parsed["business_number"] is None
        assert parsed["total_amount"] is None
    
    def test_parse_receipt_multiple_amounts(self, ocr_service):
        """Test that largest amount is selected as total"""
        receipt_text = """
        רשת יינות ביתן
        
        פריט 1: 25.00
        פריט 2: 35.00
        פריט 3: 40.00
        סה"כ: 100.00
        """
        
        parsed = ocr_service._parse_receipt_text(receipt_text)
        
        # Should select 100.00 as total (largest)
        assert parsed["total_amount"] == 100.00
    
    def test_parse_date_formats(self, ocr_service):
        """Test different date format parsing"""
        date_tests = [
            ("15/10/2024", "2024-10-15"),
            ("15.10.2024", "2024-10-15"),
            ("15-10-2024", "2024-10-15"),
            ("15/10/24", "2024-10-15"),
            ("2024/10/15", "2024-10-15"),
        ]
        
        for input_date, expected_output in date_tests:
            text = f"תאריך: {input_date}"
            parsed = ocr_service._parse_receipt_text(text)
            assert parsed["receipt_date"] == expected_output, f"Failed for {input_date}"
    
    def test_parse_business_number_formats(self, ocr_service):
        """Test different business number format variations"""
        business_patterns = [
            "ח.פ: 123456789",
            "ח.פ.: 123456789",
            "עוסק מורשה: 123456789",
            "ע.מ: 123456789",
            "Business: 123456789",
        ]
        
        for pattern in business_patterns:
            parsed = ocr_service._parse_receipt_text(pattern)
            assert parsed["business_number"] == "123456789", f"Failed for {pattern}"
    
    def test_confidence_scores_structure(self, ocr_service):
        """Test that confidence scores are properly structured"""
        text = """
        Test Vendor
        ח.פ: 123456789
        קבלה: 123
        01/01/2024
        סה"כ: 100.00
        מע"מ: 17.00
        """
        
        parsed = ocr_service._parse_receipt_text(text)
        
        # All confidence keys should exist
        expected_keys = [
            "vendor_name", "business_number", "receipt_number",
            "receipt_date", "total_amount", "vat_amount"
        ]
        
        for key in expected_keys:
            assert key in parsed["confidence"]
            assert isinstance(parsed["confidence"][key], float)
            assert 0.0 <= parsed["confidence"][key] <= 1.0
    
    @pytest.mark.asyncio
    async def test_extract_text_from_url_success(self, ocr_service):
        """Test successful OCR extraction from URL"""
        mock_response = Mock()
        mock_response.error.message = ""
        mock_response.full_text_annotation.text = "Test Receipt\nסה״כ: 100.00"
        mock_response.full_text_annotation.pages = [Mock()]
        
        ocr_service.client.document_text_detection = Mock(return_value=mock_response)
        
        with patch('requests.get') as mock_get:
            mock_get.return_value.content = b"fake_image_data"
            mock_get.return_value.raise_for_status = Mock()
            
            result = await ocr_service.extract_text_from_url("https://s3.example.com/image.jpg")
        
        assert result["success"] is True
        assert "full_text" in result
        assert "parsed_data" in result
        assert result["full_text"] == "Test Receipt\nסה״כ: 100.00"
    
    @pytest.mark.asyncio
    async def test_extract_text_from_url_api_error(self, ocr_service):
        """Test OCR extraction with Vision API error"""
        mock_response = Mock()
        mock_response.error.message = "API quota exceeded"
        
        ocr_service.client.document_text_detection = Mock(return_value=mock_response)
        
        with patch('requests.get') as mock_get:
            mock_get.return_value.content = b"fake_image_data"
            mock_get.return_value.raise_for_status = Mock()
            
            result = await ocr_service.extract_text_from_url("https://s3.example.com/image.jpg")
        
        assert result["success"] is False
        assert "error" in result
    
    @pytest.mark.asyncio
    async def test_extract_text_from_url_network_error(self, ocr_service):
        """Test OCR extraction with network error"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Network timeout")
            
            result = await ocr_service.extract_text_from_url("https://s3.example.com/image.jpg")
        
        assert result["success"] is False
        assert "error" in result
    
    @pytest.mark.asyncio
    async def test_retry_extraction_success_on_first_attempt(self, ocr_service):
        """Test retry logic succeeds on first attempt"""
        mock_result = {
            "success": True,
            "full_text": "Test",
            "parsed_data": {},
            "raw_response": {}
        }
        
        ocr_service.extract_text_from_url = AsyncMock(return_value=mock_result)
        
        result = await ocr_service.retry_extraction("https://example.com/image.jpg")
        
        assert result["success"] is True
        assert ocr_service.extract_text_from_url.call_count == 1
    
    @pytest.mark.asyncio
    async def test_retry_extraction_succeeds_after_retries(self, ocr_service):
        """Test retry logic succeeds after failures"""
        # First two calls fail, third succeeds
        ocr_service.extract_text_from_url = AsyncMock(
            side_effect=[
                {"success": False, "error": "Temp error"},
                {"success": False, "error": "Temp error"},
                {"success": True, "full_text": "Success", "parsed_data": {}}
            ]
        )
        
        with patch('asyncio.sleep', new=AsyncMock()):  # Mock sleep to speed up test
            result = await ocr_service.retry_extraction("https://example.com/image.jpg")
        
        assert result["success"] is True
        assert ocr_service.extract_text_from_url.call_count == 3
    
    @pytest.mark.asyncio
    async def test_retry_extraction_fails_after_max_attempts(self, ocr_service):
        """Test retry logic gives up after max attempts"""
        ocr_service.extract_text_from_url = AsyncMock(
            return_value={"success": False, "error": "Persistent error"}
        )
        
        with patch('asyncio.sleep', new=AsyncMock()):
            result = await ocr_service.retry_extraction("https://example.com/image.jpg")
        
        assert result["success"] is False
        assert ocr_service.extract_text_from_url.call_count == 3  # Max attempts
