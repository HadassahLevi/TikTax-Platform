"""
Integration Tests for Receipt Upload Endpoints
Tests file upload, validation, and processing status
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
import io
from PIL import Image

from app.main import app
from app.models.receipt import Receipt, ReceiptStatus
from app.models.user import User, SubscriptionPlan


class TestReceiptUpload:
    """Test suite for receipt upload endpoint"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def auth_headers(self):
        """Mock authentication headers"""
        # In real tests, use actual token generation
        return {"Authorization": "Bearer test_token"}
    
    @pytest.fixture
    def sample_image_file(self):
        """Generate sample image file"""
        img = Image.new('RGB', (800, 600), color='blue')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        return ('receipt.jpg', img_bytes, 'image/jpeg')
    
    @pytest.fixture
    def mock_user(self):
        """Create mock user"""
        user = Mock(spec=User)
        user.id = 1
        user.email = "test@example.com"
        user.subscription_plan = SubscriptionPlan.FREE
        user.receipt_limit = 50
        user.receipts_used_this_month = 5
        return user
    
    @pytest.mark.asyncio
    @patch('app.api.v1.endpoints.receipts.get_current_user')
    @patch('app.api.v1.endpoints.receipts.storage_service.upload_file')
    @patch('app.api.v1.endpoints.receipts.receipt_service.process_receipt')
    async def test_upload_receipt_success(
        self, 
        mock_process, 
        mock_upload, 
        mock_get_user,
        client, 
        auth_headers, 
        sample_image_file,
        mock_user
    ):
        """Test successful receipt upload"""
        # Setup mocks
        mock_get_user.return_value = mock_user
        mock_upload.return_value = ("https://s3.amazonaws.com/receipts/test.jpg", 50000)
        mock_process.return_value = AsyncMock()
        
        # Make request
        files = {'file': sample_image_file}
        response = client.post(
            "/api/v1/receipts/upload",
            files=files,
            headers=auth_headers
        )
        
        # Assertions
        assert response.status_code == 201
        data = response.json()
        assert data['receipt_id'] is not None
        assert data['status'] == 'processing'
        assert 'הקבלה הועלתה בהצלחה' in data['message']
        
        # Verify storage service called
        mock_upload.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('app.api.v1.endpoints.receipts.get_current_user')
    async def test_upload_receipt_invalid_file_type(
        self,
        mock_get_user,
        client,
        auth_headers,
        mock_user
    ):
        """Test upload with invalid file type"""
        mock_get_user.return_value = mock_user
        
        # Create text file
        text_file = ('document.txt', io.BytesIO(b"Not an image"), 'text/plain')
        
        files = {'file': text_file}
        response = client.post(
            "/api/v1/receipts/upload",
            files=files,
            headers=auth_headers
        )
        
        # Should reject
        assert response.status_code == 400
        assert 'סוג קובץ לא נתמך' in response.json()['detail']
    
    @pytest.mark.asyncio
    @patch('app.api.v1.endpoints.receipts.get_current_user')
    async def test_upload_receipt_file_too_large(
        self,
        mock_get_user,
        client,
        auth_headers,
        mock_user
    ):
        """Test upload with file exceeding size limit"""
        mock_get_user.return_value = mock_user
        
        # Create large file (11 MB)
        large_data = b'x' * (11 * 1024 * 1024)
        large_file = ('large.jpg', io.BytesIO(large_data), 'image/jpeg')
        
        files = {'file': large_file}
        response = client.post(
            "/api/v1/receipts/upload",
            files=files,
            headers=auth_headers
        )
        
        # Should reject
        assert response.status_code == 413
        assert 'קובץ גדול מדי' in response.json()['detail']
    
    @pytest.mark.asyncio
    @patch('app.api.v1.endpoints.receipts.get_current_user')
    async def test_upload_receipt_file_too_small(
        self,
        mock_get_user,
        client,
        auth_headers,
        mock_user
    ):
        """Test upload with file below minimum size"""
        mock_get_user.return_value = mock_user
        
        # Create tiny file (5 KB)
        small_data = b'x' * (5 * 1024)
        small_file = ('small.jpg', io.BytesIO(small_data), 'image/jpeg')
        
        files = {'file': small_file}
        response = client.post(
            "/api/v1/receipts/upload",
            files=files,
            headers=auth_headers
        )
        
        # Should reject
        assert response.status_code == 400
        assert 'קובץ קטן מדי' in response.json()['detail']
    
    @pytest.mark.asyncio
    @patch('app.api.v1.endpoints.receipts.get_current_user')
    @patch('app.api.v1.endpoints.receipts.check_subscription_limit')
    async def test_upload_receipt_subscription_limit_exceeded(
        self,
        mock_check_limit,
        mock_get_user,
        client,
        auth_headers,
        sample_image_file,
        mock_user
    ):
        """Test upload when subscription limit is exceeded"""
        mock_get_user.return_value = mock_user
        mock_check_limit.side_effect = HTTPException(
            status_code=402,
            detail="הגעת למכסת הקבלות החודשית"
        )
        
        files = {'file': sample_image_file}
        response = client.post(
            "/api/v1/receipts/upload",
            files=files,
            headers=auth_headers
        )
        
        # Should reject with payment required
        assert response.status_code == 402
        assert 'מכסת הקבלות' in response.json()['detail']
    
    @pytest.mark.asyncio
    @patch('app.api.v1.endpoints.receipts.get_current_user')
    @patch('app.api.v1.endpoints.receipts.storage_service.upload_file')
    async def test_upload_receipt_storage_failure(
        self,
        mock_upload,
        mock_get_user,
        client,
        auth_headers,
        sample_image_file,
        mock_user
    ):
        """Test upload when S3 storage fails"""
        mock_get_user.return_value = mock_user
        mock_upload.side_effect = Exception("S3 upload failed")
        
        files = {'file': sample_image_file}
        response = client.post(
            "/api/v1/receipts/upload",
            files=files,
            headers=auth_headers
        )
        
        # Should return 500
        assert response.status_code == 500
        assert 'העלאת הקבלה נכשלה' in response.json()['detail']


class TestReceiptProcessingStatus:
    """Test suite for processing status endpoint"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def auth_headers(self):
        """Mock authentication headers"""
        return {"Authorization": "Bearer test_token"}
    
    @pytest.fixture
    def mock_user(self):
        """Create mock user"""
        user = Mock(spec=User)
        user.id = 1
        user.email = "test@example.com"
        return user
    
    @pytest.fixture
    def mock_receipt_processing(self):
        """Create mock receipt in processing state"""
        receipt = Mock(spec=Receipt)
        receipt.id = 1
        receipt.user_id = 1
        receipt.status = ReceiptStatus.PROCESSING
        receipt.ocr_data = None
        return receipt
    
    @pytest.fixture
    def mock_receipt_review(self):
        """Create mock receipt in review state"""
        receipt = Mock(spec=Receipt)
        receipt.id = 1
        receipt.user_id = 1
        receipt.status = ReceiptStatus.REVIEW
        receipt.ocr_data = {
            'vendor_name': 'Test Vendor',
            'total_amount': 100.0
        }
        return receipt
    
    @pytest.mark.asyncio
    @patch('app.api.v1.endpoints.receipts.get_current_user')
    async def test_get_status_processing(
        self,
        mock_get_user,
        client,
        auth_headers,
        mock_user,
        mock_receipt_processing,
        db_session
    ):
        """Test status check for processing receipt"""
        mock_get_user.return_value = mock_user
        
        # Mock database query
        with patch.object(db_session, 'query') as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = mock_receipt_processing
            
            response = client.get(
                "/api/v1/receipts/1/status",
                headers=auth_headers
            )
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data['receipt_id'] == 1
            assert data['status'] == 'processing'
            assert data['progress'] == 50
            assert 'מעבד' in data['message']
            assert data['ocr_data'] is None
    
    @pytest.mark.asyncio
    @patch('app.api.v1.endpoints.receipts.get_current_user')
    async def test_get_status_review(
        self,
        mock_get_user,
        client,
        auth_headers,
        mock_user,
        mock_receipt_review,
        db_session
    ):
        """Test status check for receipt ready for review"""
        mock_get_user.return_value = mock_user
        
        # Mock database query
        with patch.object(db_session, 'query') as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = mock_receipt_review
            
            response = client.get(
                "/api/v1/receipts/1/status",
                headers=auth_headers
            )
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data['receipt_id'] == 1
            assert data['status'] == 'review'
            assert data['progress'] == 80
            assert data['ocr_data'] is not None
            assert data['ocr_data']['vendor_name'] == 'Test Vendor'
    
    @pytest.mark.asyncio
    @patch('app.api.v1.endpoints.receipts.get_current_user')
    async def test_get_status_not_found(
        self,
        mock_get_user,
        client,
        auth_headers,
        mock_user,
        db_session
    ):
        """Test status check for non-existent receipt"""
        mock_get_user.return_value = mock_user
        
        # Mock database query returning None
        with patch.object(db_session, 'query') as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = None
            
            response = client.get(
                "/api/v1/receipts/999/status",
                headers=auth_headers
            )
            
            # Should return 404
            assert response.status_code == 404
            assert 'קבלה לא נמצאה' in response.json()['detail']
    
    @pytest.mark.asyncio
    @patch('app.api.v1.endpoints.receipts.get_current_user')
    async def test_get_status_wrong_user(
        self,
        mock_get_user,
        client,
        auth_headers,
        mock_receipt_processing,
        db_session
    ):
        """Test status check for receipt belonging to different user"""
        # User with different ID
        other_user = Mock(spec=User)
        other_user.id = 999
        mock_get_user.return_value = other_user
        
        # Mock database query returning None (due to user_id filter)
        with patch.object(db_session, 'query') as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = None
            
            response = client.get(
                "/api/v1/receipts/1/status",
                headers=auth_headers
            )
            
            # Should return 404 (not exposing that receipt exists)
            assert response.status_code == 404
