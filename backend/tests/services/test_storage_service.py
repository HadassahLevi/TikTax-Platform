"""
Unit Tests for Storage Service
Tests S3 file upload, deletion, and presigned URL generation
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError
from PIL import Image
import io

from app.services.storage_service import StorageService


class TestStorageService:
    """Test suite for StorageService"""
    
    @pytest.fixture
    def storage_service(self):
        """Create StorageService instance with mocked S3 client"""
        with patch('app.services.storage_service.boto3.client') as mock_boto:
            service = StorageService()
            service.s3_client = Mock()
            service.bucket_name = "test-bucket"
            return service
    
    @pytest.fixture
    def sample_image(self):
        """Generate sample image bytes"""
        img = Image.new('RGB', (800, 600), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        return img_bytes.read()
    
    def test_generate_unique_filename(self, storage_service):
        """Test unique filename generation"""
        filename = storage_service._generate_unique_filename("receipt.jpg", 123)
        
        # Should contain user ID
        assert "receipts/123/" in filename
        
        # Should have year/month structure
        assert len(filename.split('/')) == 5  # receipts/user_id/year/month/uuid.ext
        
        # Should preserve extension
        assert filename.endswith('.jpg')
    
    def test_generate_unique_filename_no_extension(self, storage_service):
        """Test filename generation without extension"""
        filename = storage_service._generate_unique_filename("receipt", 123)
        
        # Should default to .jpg
        assert filename.endswith('.jpg')
    
    def test_optimize_image_resize(self, storage_service):
        """Test image optimization with resize"""
        # Create large image
        large_img = Image.new('RGB', (3000, 3000), color='blue')
        img_bytes = io.BytesIO()
        large_img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        optimized = storage_service._optimize_image(img_bytes.read(), 'image/png')
        
        # Check optimized image
        optimized_img = Image.open(io.BytesIO(optimized))
        
        # Should be resized
        assert optimized_img.width <= 2000
        assert optimized_img.height <= 2000
        
        # Should be JPEG
        assert optimized_img.format == 'JPEG'
    
    def test_optimize_image_rgba_conversion(self, storage_service):
        """Test RGBA to RGB conversion"""
        # Create RGBA image
        rgba_img = Image.new('RGBA', (500, 500), color=(255, 0, 0, 128))
        img_bytes = io.BytesIO()
        rgba_img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        optimized = storage_service._optimize_image(img_bytes.read(), 'image/png')
        
        # Check optimized image
        optimized_img = Image.open(io.BytesIO(optimized))
        
        # Should be RGB (not RGBA)
        assert optimized_img.mode == 'RGB'
    
    def test_optimize_image_handles_error(self, storage_service):
        """Test graceful error handling in optimization"""
        # Invalid image data
        invalid_data = b"not an image"
        
        result = storage_service._optimize_image(invalid_data, 'image/jpeg')
        
        # Should return original data on error
        assert result == invalid_data
    
    @pytest.mark.asyncio
    async def test_upload_file_success(self, storage_service, sample_image):
        """Test successful file upload"""
        # Mock S3 client
        storage_service.s3_client.put_object = Mock()
        
        url, size = await storage_service.upload_file(
            file_content=sample_image,
            filename="test_receipt.jpg",
            user_id=123,
            mime_type="image/jpeg"
        )
        
        # Should return URL and size
        assert url.startswith("https://test-bucket.s3.")
        assert size > 0
        
        # Should call S3 put_object
        storage_service.s3_client.put_object.assert_called_once()
        
        # Check put_object arguments
        call_args = storage_service.s3_client.put_object.call_args[1]
        assert call_args['Bucket'] == 'test-bucket'
        assert call_args['ContentType'] == 'image/jpeg'
        assert call_args['ServerSideEncryption'] == 'AES256'
        assert 'user_id' in call_args['Metadata']
    
    @pytest.mark.asyncio
    async def test_upload_file_client_error(self, storage_service, sample_image):
        """Test upload failure with ClientError"""
        # Mock S3 client to raise error
        storage_service.s3_client.put_object = Mock(
            side_effect=ClientError(
                {'Error': {'Code': 'AccessDenied', 'Message': 'Access Denied'}},
                'PutObject'
            )
        )
        
        with pytest.raises(Exception) as exc_info:
            await storage_service.upload_file(
                file_content=sample_image,
                filename="test.jpg",
                user_id=123,
                mime_type="image/jpeg"
            )
        
        assert "העלאת קובץ נכשלה" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_delete_file_success(self, storage_service):
        """Test successful file deletion"""
        # Mock S3 client
        storage_service.s3_client.delete_object = Mock()
        
        file_url = "https://test-bucket.s3.eu-west-1.amazonaws.com/receipts/123/2024/11/test.jpg"
        
        result = await storage_service.delete_file(file_url)
        
        # Should return True
        assert result is True
        
        # Should call S3 delete_object
        storage_service.s3_client.delete_object.assert_called_once_with(
            Bucket='test-bucket',
            Key='receipts/123/2024/11/test.jpg'
        )
    
    @pytest.mark.asyncio
    async def test_delete_file_error(self, storage_service):
        """Test delete failure"""
        # Mock S3 client to raise error
        storage_service.s3_client.delete_object = Mock(
            side_effect=Exception("Delete failed")
        )
        
        file_url = "https://test-bucket.s3.eu-west-1.amazonaws.com/receipts/123/2024/11/test.jpg"
        
        result = await storage_service.delete_file(file_url)
        
        # Should return False on error
        assert result is False
    
    @pytest.mark.asyncio
    async def test_generate_presigned_url_success(self, storage_service):
        """Test presigned URL generation"""
        # Mock S3 client
        storage_service.s3_client.generate_presigned_url = Mock(
            return_value="https://presigned-url.com/test.jpg?signature=xyz"
        )
        
        file_url = "https://test-bucket.s3.eu-west-1.amazonaws.com/receipts/123/2024/11/test.jpg"
        
        presigned_url = await storage_service.generate_presigned_url(file_url, expires_in=7200)
        
        # Should return presigned URL
        assert presigned_url.startswith("https://presigned-url.com/")
        
        # Should call generate_presigned_url
        storage_service.s3_client.generate_presigned_url.assert_called_once_with(
            'get_object',
            Params={
                'Bucket': 'test-bucket',
                'Key': 'receipts/123/2024/11/test.jpg'
            },
            ExpiresIn=7200
        )
    
    @pytest.mark.asyncio
    async def test_generate_presigned_url_error(self, storage_service):
        """Test presigned URL generation error fallback"""
        # Mock S3 client to raise error
        storage_service.s3_client.generate_presigned_url = Mock(
            side_effect=Exception("Presigned URL failed")
        )
        
        file_url = "https://test-bucket.s3.eu-west-1.amazonaws.com/receipts/123/2024/11/test.jpg"
        
        presigned_url = await storage_service.generate_presigned_url(file_url)
        
        # Should return original URL as fallback
        assert presigned_url == file_url
