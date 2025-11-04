"""
Storage Service
AWS S3 integration for secure file storage with image optimization
"""

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from app.core.config import settings
import logging
from typing import Optional, BinaryIO
from datetime import datetime, timedelta
import uuid
from PIL import Image
import io

logger = logging.getLogger(__name__)


class StorageService:
    """
    AWS S3 Storage Service
    Handles receipt image uploads with optimization, secure storage, and presigned URLs
    """
    
    def __init__(self):
        """Initialize S3 client with credentials from settings"""
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION,
            config=Config(signature_version='s3v4')
        )
        self.bucket_name = settings.AWS_S3_BUCKET
    
    def _generate_unique_filename(self, original_filename: str, user_id: int) -> str:
        """
        Generate unique S3 key for file
        Format: receipts/{user_id}/{year}/{month}/{uuid}.{extension}
        
        Args:
            original_filename: Original uploaded filename
            user_id: User ID for folder structure
            
        Returns:
            str: S3 key path
        """
        now = datetime.utcnow()
        file_uuid = str(uuid.uuid4())
        extension = original_filename.split('.')[-1] if '.' in original_filename else 'jpg'
        
        return f"receipts/{user_id}/{now.year}/{now.month:02d}/{file_uuid}.{extension}"
    
    def _optimize_image(self, file_content: bytes, mime_type: str) -> bytes:
        """
        Optimize image for storage:
        - Resize if larger than 2000x2000
        - Convert to JPEG with 85% quality
        - Strip EXIF data for privacy
        
        Args:
            file_content: Raw image bytes
            mime_type: Original MIME type
            
        Returns:
            bytes: Optimized image bytes
        """
        try:
            img = Image.open(io.BytesIO(file_content))
            
            # Resize if too large
            max_size = (2000, 2000)
            if img.width > max_size[0] or img.height > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                logger.info(f"Resized image from {img.size} to fit {max_size}")
            
            # Convert to RGB if needed (RGBA, P, LA modes)
            if img.mode in ('RGBA', 'P', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save as optimized JPEG
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            optimized_content = output.read()
            logger.info(f"Image optimized: {len(file_content)} bytes → {len(optimized_content)} bytes")
            
            return optimized_content
            
        except Exception as e:
            logger.warning(f"Image optimization failed: {str(e)}. Using original.")
            return file_content
    
    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        user_id: int,
        mime_type: str
    ) -> tuple[str, int]:
        """
        Upload file to S3 with optimization and encryption
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            user_id: User ID for folder structure
            mime_type: Original MIME type
            
        Returns:
            tuple: (s3_url, file_size)
            
        Raises:
            Exception: If upload fails
        """
        try:
            # Optimize image
            optimized_content = self._optimize_image(file_content, mime_type)
            file_size = len(optimized_content)
            
            # Generate unique filename
            s3_key = self._generate_unique_filename(filename, user_id)
            
            # Upload to S3 with server-side encryption
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=optimized_content,
                ContentType='image/jpeg',
                ServerSideEncryption='AES256',
                Metadata={
                    'user_id': str(user_id),
                    'original_filename': filename,
                    'upload_date': datetime.utcnow().isoformat()
                }
            )
            
            # Generate public URL
            s3_url = f"https://{self.bucket_name}.s3.{settings.AWS_S3_REGION}.amazonaws.com/{s3_key}"
            
            logger.info(f"File uploaded successfully: {s3_key} ({file_size} bytes)")
            return s3_url, file_size
            
        except ClientError as e:
            logger.error(f"S3 upload failed: {str(e)}")
            raise Exception("העלאת קובץ נכשלה. נסה שוב.")
        except Exception as e:
            logger.error(f"Unexpected error during upload: {str(e)}")
            raise Exception("העלאת קובץ נכשלה. נסה שוב.")
    
    async def delete_file(self, file_url: str) -> bool:
        """
        Delete file from S3
        
        Args:
            file_url: Full S3 URL to the file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Extract S3 key from URL
            s3_key = file_url.split(f"{self.bucket_name}.s3.{settings.AWS_S3_REGION}.amazonaws.com/")[1]
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            logger.info(f"File deleted: {s3_key}")
            return True
            
        except Exception as e:
            logger.error(f"S3 delete failed: {str(e)}")
            return False
    
    async def generate_presigned_url(self, file_url: str, expires_in: int = 3600) -> str:
        """
        Generate presigned URL for temporary access
        Default expiration: 1 hour
        
        Args:
            file_url: Full S3 URL
            expires_in: Expiration time in seconds
            
        Returns:
            str: Presigned URL or original URL if generation fails
        """
        try:
            # Extract S3 key from URL
            s3_key = file_url.split(f"{self.bucket_name}.s3.{settings.AWS_S3_REGION}.amazonaws.com/")[1]
            
            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expires_in
            )
            
            logger.info(f"Generated presigned URL for {s3_key}")
            return presigned_url
            
        except Exception as e:
            logger.error(f"Presigned URL generation failed: {str(e)}")
            return file_url  # Return original URL as fallback


# Global storage service instance
storage_service = StorageService()
        # TODO: Implement presigned URL generation
        pass
