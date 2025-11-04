"""
Receipt Service
Handles receipt processing, storage, and management
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.models.receipt import Receipt, ReceiptStatus
from app.services.ocr_service import ocr_service

logger = logging.getLogger(__name__)


class ReceiptService:
    """Receipt service layer"""
    
    async def process_receipt(self, receipt_id: int, db: Session) -> None:
        """
        Process receipt with OCR in background
        
        Args:
            receipt_id: Receipt ID to process
            db: Database session
        """
        try:
            receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
            if not receipt:
                logger.error(f"Receipt not found: {receipt_id}")
                return
            
            # Update status to processing
            receipt.status = ReceiptStatus.PROCESSING
            receipt.processing_started_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Starting OCR processing for receipt {receipt_id}")
            
            # Perform OCR
            ocr_result = await ocr_service.extract_text_from_image(receipt.file_url)
            
            if ocr_result.get('success'):
                # Update receipt with OCR data
                receipt.ocr_data = ocr_result.get('raw_data')
                receipt.vendor_name = ocr_result.get('vendor_name')
                receipt.business_number = ocr_result.get('business_number')
                receipt.receipt_number = ocr_result.get('receipt_number')
                receipt.receipt_date = ocr_result.get('receipt_date')
                receipt.total_amount = ocr_result.get('total_amount')
                receipt.vat_amount = ocr_result.get('vat_amount')
                receipt.pre_vat_amount = ocr_result.get('pre_vat_amount')
                receipt.confidence_score = ocr_result.get('confidence_score')
                
                receipt.status = ReceiptStatus.REVIEW
                receipt.processing_completed_at = datetime.utcnow()
                
                logger.info(f"OCR completed successfully for receipt {receipt_id}")
            else:
                receipt.status = ReceiptStatus.FAILED
                receipt.processing_completed_at = datetime.utcnow()
                logger.error(f"OCR failed for receipt {receipt_id}: {ocr_result.get('error')}")
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error processing receipt {receipt_id}: {str(e)}")
            receipt.status = ReceiptStatus.FAILED
            receipt.processing_completed_at = datetime.utcnow()
            db.commit()
    
    @staticmethod
    def create_receipt(db: Session, user_id: str, **kwargs) -> Receipt:
        """
        Create new receipt
        
        Args:
            db: Database session
            user_id: User ID
            **kwargs: Receipt fields
            
        Returns:
            Created receipt
        """
        # TODO: Implement receipt creation
        pass
    
    @staticmethod
    def get_user_receipts(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 50,
        category_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Receipt]:
        """
        Get user receipts with filtering
        
        Args:
            db: Database session
            user_id: User ID
            skip: Pagination offset
            limit: Pagination limit
            category_id: Filter by category
            start_date: Filter by start date
            end_date: Filter by end date
            
        Returns:
            List of receipts
        """
        # TODO: Implement receipt listing with filters
        pass
    
    @staticmethod
    def update_receipt(db: Session, receipt_id: str, user_id: str, **kwargs) -> Receipt:
        """
        Update receipt
        
        Args:
            db: Database session
            receipt_id: Receipt ID
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Updated receipt
        """
        # TODO: Implement receipt update with edit history tracking
        pass
    
    @staticmethod
    def delete_receipt(db: Session, receipt_id: str, user_id: str) -> None:
        """
        Soft delete receipt
        
        Args:
            db: Database session
            receipt_id: Receipt ID
            user_id: User ID
        """
        # TODO: Implement soft deletion
        pass


# Global receipt service instance
receipt_service = ReceiptService()
