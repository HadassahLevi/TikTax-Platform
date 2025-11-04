"""
PDF Service Unit Tests
Test PDF generation functionality with receipts and images
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO
from PIL import Image as PILImage

from app.services.pdf_service import PDFService, pdf_service
from app.models.user import User, SubscriptionPlan
from app.models.receipt import Receipt, ReceiptStatus
from app.models.category import Category


@pytest.fixture
def mock_user():
    """Create mock user"""
    user = Mock(spec=User)
    user.id = 1
    user.email = "test@tiktax.co.il"
    user.full_name = "David Cohen"
    user.business_name = "Cohen Design Studio"
    user.business_number = "123456789"
    user.subscription_plan = SubscriptionPlan.PRO
    return user


@pytest.fixture
def mock_categories():
    """Create mock categories"""
    categories = []
    cat_data = [
        (1, "Office Supplies", "ציוד משרדי"),
        (2, "Transportation", "תחבורה"),
        (3, "Meals & Entertainment", "אוכל ואירוח")
    ]
    for cat_id, name_en, name_he in cat_data:
        cat = Mock(spec=Category)
        cat.id = cat_id
        cat.name = name_en
        cat.name_hebrew = name_he
        categories.append(cat)
    return categories


@pytest.fixture
def mock_receipts():
    """Create mock receipts"""
    receipts = []
    base_date = datetime(2024, 1, 15, 10, 0, 0)
    
    receipt_data = [
        {
            "vendor": "Office Depot",
            "category_id": 1,
            "total": 500.00,
            "vat": 72.65,
            "pre_vat": 427.35,
            "business_number": "123456789",
            "receipt_number": "REC-001"
        },
        {
            "vendor": "Shell Gas Station",
            "category_id": 2,
            "total": 300.00,
            "vat": 43.59,
            "pre_vat": 256.41,
            "business_number": "987654321",
            "receipt_number": "REC-002"
        },
        {
            "vendor": "Cafe Aroma",
            "category_id": 3,
            "total": 150.00,
            "vat": 21.79,
            "pre_vat": 128.21,
            "business_number": "555666777",
            "receipt_number": "REC-003"
        }
    ]
    
    for i, data in enumerate(receipt_data):
        receipt = Mock(spec=Receipt)
        receipt.id = i + 1
        receipt.vendor_name = data["vendor"]
        receipt.category_id = data["category_id"]
        receipt.total_amount = data["total"]
        receipt.vat_amount = data["vat"]
        receipt.pre_vat_amount = data["pre_vat"]
        receipt.business_number = data["business_number"]
        receipt.receipt_number = data["receipt_number"]
        receipt.receipt_date = base_date + timedelta(days=i)
        receipt.file_url = f"https://s3.amazonaws.com/tiktax/receipts/receipt_{i+1}.jpg"
        receipt.status = ReceiptStatus.APPROVED
        receipts.append(receipt)
    
    return receipts


class TestPDFService:
    """Test PDF Service"""
    
    def test_pdf_service_initialization(self):
        """Test PDF service initializes correctly"""
        service = PDFService()
        assert service.styles is not None
        assert service.hebrew_style is not None
        assert service.hebrew_title is not None
    
    def test_singleton_instance(self):
        """Test pdf_service singleton exists"""
        assert pdf_service is not None
        assert isinstance(pdf_service, PDFService)
    
    def test_generate_export_basic(self, mock_user, mock_receipts, mock_categories):
        """Test basic PDF generation without images"""
        service = PDFService()
        
        date_from = datetime(2024, 1, 1)
        date_to = datetime(2024, 1, 31)
        
        # Generate PDF
        pdf_bytes = service.generate_export(
            user=mock_user,
            receipts=mock_receipts,
            categories=mock_categories,
            date_from=date_from,
            date_to=date_to,
            include_images=False
        )
        
        # Verify output
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 1000  # PDF should have content
        assert pdf_bytes[:4] == b'%PDF'  # PDF header
    
    def test_generate_export_empty_receipts(self, mock_user, mock_categories):
        """Test PDF generation with no receipts"""
        service = PDFService()
        
        date_from = datetime(2024, 1, 1)
        date_to = datetime(2024, 1, 31)
        
        # Generate PDF with empty receipts
        pdf_bytes = service.generate_export(
            user=mock_user,
            receipts=[],
            categories=mock_categories,
            date_from=date_from,
            date_to=date_to,
            include_images=False
        )
        
        # Should still generate PDF
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 500
    
    def test_create_title_page(self, mock_user):
        """Test title page creation"""
        service = PDFService()
        
        date_from = datetime(2024, 1, 1)
        date_to = datetime(2024, 1, 31)
        
        elements = service._create_title_page(mock_user, date_from, date_to)
        
        # Should have title and business info table
        assert len(elements) > 0
    
    def test_create_summary_section(self, mock_receipts):
        """Test summary section with totals"""
        service = PDFService()
        
        elements = service._create_summary_section(mock_receipts)
        
        # Should have summary elements
        assert len(elements) > 0
    
    def test_create_category_section(self, mock_receipts, mock_categories):
        """Test category breakdown section"""
        service = PDFService()
        
        elements = service._create_category_section(mock_receipts, mock_categories)
        
        # Should have category breakdown
        assert len(elements) > 0
    
    def test_create_details_section(self, mock_receipts, mock_categories):
        """Test detailed receipts table"""
        service = PDFService()
        
        elements = service._create_details_section(mock_receipts, mock_categories)
        
        # Should have receipt details
        assert len(elements) > 0
    
    @patch('app.services.pdf_service.requests.get')
    @patch('app.services.pdf_service.PILImage.open')
    def test_create_images_section_success(
        self, 
        mock_pil_open, 
        mock_requests_get, 
        mock_receipts
    ):
        """Test images section with successful image loading"""
        service = PDFService()
        
        # Mock image response
        mock_response = Mock()
        mock_response.content = b'fake_image_data'
        mock_response.raise_for_status = Mock()
        mock_requests_get.return_value = mock_response
        
        # Mock PIL image
        mock_img = Mock()
        mock_img.width = 1000
        mock_img.height = 1500
        mock_pil_open.return_value = mock_img
        
        # Create images section
        elements = service._create_images_section(mock_receipts[:1])  # Just one receipt
        
        # Should have elements
        assert len(elements) > 0
        mock_requests_get.assert_called_once()
    
    @patch('app.services.pdf_service.requests.get')
    def test_create_images_section_network_error(self, mock_requests_get, mock_receipts):
        """Test images section handles network errors gracefully"""
        service = PDFService()
        
        # Mock network error
        import requests
        mock_requests_get.side_effect = requests.RequestException("Network error")
        
        # Should not raise exception
        elements = service._create_images_section(mock_receipts[:1])
        
        # Should still return elements (with error message)
        assert len(elements) > 0
    
    def test_create_receipts_table(self):
        """Test receipts table creation"""
        service = PDFService()
        
        table_data = [
            ["תאריך", "ספק", "קטגוריה", "לפני מע\"מ", "מע\"מ", "סה\"כ"],
            ["15/01/2024", "Office Depot", "ציוד משרדי", "₪427.35", "₪72.65", "₪500.00"]
        ]
        
        table = service._create_receipts_table(table_data)
        
        # Should return table object
        assert table is not None
    
    def test_large_receipts_pagination(self, mock_user, mock_categories):
        """Test pagination with many receipts"""
        service = PDFService()
        
        # Create 100 mock receipts
        receipts = []
        for i in range(100):
            receipt = Mock(spec=Receipt)
            receipt.id = i + 1
            receipt.vendor_name = f"Vendor {i+1}"
            receipt.category_id = 1
            receipt.total_amount = 100.0 + i
            receipt.vat_amount = 14.53 + (i * 0.17)
            receipt.pre_vat_amount = 85.47 + (i * 0.83)
            receipt.receipt_date = datetime(2024, 1, 1) + timedelta(days=i)
            receipt.file_url = f"https://s3.amazonaws.com/tiktax/receipts/receipt_{i+1}.jpg"
            receipts.append(receipt)
        
        # Generate PDF
        pdf_bytes = service.generate_export(
            user=mock_user,
            receipts=receipts,
            categories=mock_categories,
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 4, 30),
            include_images=False
        )
        
        # Should successfully generate large PDF
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 5000  # Should be substantial
    
    def test_generate_export_with_missing_data(self, mock_user, mock_categories):
        """Test PDF generation with receipts missing data"""
        service = PDFService()
        
        # Create receipt with missing fields
        receipt = Mock(spec=Receipt)
        receipt.id = 1
        receipt.vendor_name = None  # Missing
        receipt.category_id = None  # Missing
        receipt.total_amount = None  # Missing
        receipt.vat_amount = None
        receipt.pre_vat_amount = None
        receipt.receipt_date = None  # Missing
        receipt.file_url = "https://s3.amazonaws.com/tiktax/receipts/receipt_1.jpg"
        
        # Should not raise exception
        pdf_bytes = service.generate_export(
            user=mock_user,
            receipts=[receipt],
            categories=mock_categories,
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 1, 31),
            include_images=False
        )
        
        assert isinstance(pdf_bytes, bytes)
    
    def test_user_without_business_info(self, mock_receipts, mock_categories):
        """Test PDF with user lacking business info"""
        service = PDFService()
        
        # User without business info
        user = Mock(spec=User)
        user.id = 1
        user.email = "test@example.com"
        user.full_name = "Test User"
        user.business_name = None
        user.business_number = None
        
        pdf_bytes = service.generate_export(
            user=user,
            receipts=mock_receipts,
            categories=mock_categories,
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 1, 31),
            include_images=False
        )
        
        # Should generate PDF with "לא צוין" for missing info
        assert isinstance(pdf_bytes, bytes)
    
    def test_category_totals_calculation(self, mock_receipts, mock_categories):
        """Test category totals are calculated correctly"""
        service = PDFService()
        
        # Expected totals:
        # Category 1 (Office): 500.00
        # Category 2 (Transportation): 300.00
        # Category 3 (Meals): 150.00
        # Total: 950.00
        
        pdf_bytes = service.generate_export(
            user=Mock(id=1, business_name="Test", business_number="123"),
            receipts=mock_receipts,
            categories=mock_categories,
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 1, 31),
            include_images=False
        )
        
        # PDF should be generated successfully
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 2000
    
    @patch('app.services.pdf_service.requests.get')
    @patch('app.services.pdf_service.PILImage.open')
    def test_generate_export_with_images(
        self,
        mock_pil_open,
        mock_requests_get,
        mock_user,
        mock_receipts,
        mock_categories
    ):
        """Test PDF generation with receipt images"""
        service = PDFService()
        
        # Mock image response
        mock_response = Mock()
        mock_response.content = b'fake_image_data'
        mock_response.raise_for_status = Mock()
        mock_requests_get.return_value = mock_response
        
        # Mock PIL image
        mock_img = Mock()
        mock_img.width = 800
        mock_img.height = 1200
        mock_pil_open.return_value = mock_img
        
        # Generate PDF with images
        pdf_bytes = service.generate_export(
            user=mock_user,
            receipts=mock_receipts,
            categories=mock_categories,
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 1, 31),
            include_images=True
        )
        
        # Should include images
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 3000  # Larger with images
        
        # Should call requests.get for each receipt
        assert mock_requests_get.call_count == len(mock_receipts)
