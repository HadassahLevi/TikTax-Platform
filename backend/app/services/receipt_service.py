"""
Receipt Service
Handles receipt processing pipeline, storage, and management
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.models.receipt import Receipt, ReceiptStatus
from app.models.category import Category
from app.services.ocr_service import ocr_service
from app.utils.validators import validate_israeli_business_number

logger = logging.getLogger(__name__)


class ReceiptService:
    """Receipt service layer for complete processing pipeline"""
    
    async def process_receipt(self, receipt_id: int, db: Session) -> None:
        """
        Complete receipt processing pipeline:
        1. Extract text via OCR
        2. Parse and validate data
        3. Categorize receipt
        4. Check for duplicates
        5. Update receipt status
        
        Args:
            receipt_id: Receipt ID to process
            db: Database session
        """
        receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
        
        if not receipt:
            logger.error(f"Receipt {receipt_id} not found")
            return
        
        try:
            logger.info(f"Starting processing for receipt {receipt_id}")
            
            # Update status to processing
            receipt.status = ReceiptStatus.PROCESSING
            receipt.processing_started_at = datetime.utcnow()
            db.commit()
            
            # Step 1: OCR Extraction with retry
            ocr_result = await ocr_service.retry_extraction(receipt.file_url)
            
            if not ocr_result["success"]:
                receipt.status = ReceiptStatus.FAILED
                receipt.processing_completed_at = datetime.utcnow()
                db.commit()
                logger.error(f"OCR failed for receipt {receipt_id}: {ocr_result.get('error')}")
                return
            
            # Step 2: Store OCR data
            parsed_data = ocr_result["parsed_data"]
            receipt.ocr_data = ocr_result
            
            # Step 3: Populate receipt fields
            receipt.vendor_name = parsed_data.get("vendor_name")
            receipt.business_number = parsed_data.get("business_number")
            receipt.receipt_number = parsed_data.get("receipt_number")
            
            # Parse date
            if parsed_data.get("receipt_date"):
                try:
                    receipt.receipt_date = datetime.strptime(
                        parsed_data["receipt_date"], 
                        "%Y-%m-%d"
                    )
                except:
                    logger.warning(f"Failed to parse date: {parsed_data.get('receipt_date')}")
            
            # Financial data
            receipt.total_amount = parsed_data.get("total_amount")
            receipt.vat_amount = parsed_data.get("vat_amount")
            receipt.pre_vat_amount = parsed_data.get("pre_vat_amount")
            
            # Calculate average confidence
            confidences = list(parsed_data.get("confidence", {}).values())
            receipt.confidence_score = sum(confidences) / len(confidences) if confidences else 0.0
            
            # Step 4: Auto-categorize
            category_id = await self._categorize_receipt(receipt, db)
            if category_id:
                receipt.category_id = category_id
                logger.info(f"Receipt {receipt_id} auto-categorized to category {category_id}")
            
            # Step 5: Check for duplicates
            is_duplicate = await self._check_duplicate(receipt, db)
            if is_duplicate:
                receipt.status = ReceiptStatus.DUPLICATE
                receipt.is_duplicate = True
                logger.warning(f"Receipt {receipt_id} detected as duplicate")
            else:
                receipt.status = ReceiptStatus.REVIEW
            
            receipt.processing_completed_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Receipt {receipt_id} processed successfully. Status: {receipt.status.value}")
            
        except Exception as e:
            logger.error(f"Processing failed for receipt {receipt_id}: {str(e)}", exc_info=True)
            receipt.status = ReceiptStatus.FAILED
            receipt.processing_completed_at = datetime.utcnow()
            db.commit()
    
    async def _categorize_receipt(self, receipt: Receipt, db: Session) -> Optional[int]:
        """
        Auto-categorize receipt based on vendor name
        Simple keyword matching (can be improved with ML in future)
        
        Args:
            receipt: Receipt object
            db: Database session
            
        Returns:
            Category ID if match found, None otherwise
        """
        if not receipt.vendor_name:
            return None
        
        vendor_lower = receipt.vendor_name.lower()
        
        # Category keyword mappings (Hebrew and English)
        category_keywords = {
            "מזון ושתייה": ["מסעדה", "קפה", "פיצה", "המבורגר", "סושי", "מזון", "מאפה", "בית קפה", "restaurant", "cafe"],
            "תחבורה": ["דלק", "דיזל", "תדלוק", "מונית", "אוטובוס", "רכבת", "חניה", "paz", "delek", "sonol", "parking"],
            "ציוד משרדי": ["משרד", "נייר", "מדפסת", "מחשב", "ציוד", "office", "depot", "מכשירים"],
            "שיווק ופרסום": ["פרסום", "שיווק", "גוגל", "פייסבוק", "אינסטגרם", "google", "facebook", "meta", "ads"],
            "משכורות": ["משכורת", "שכר", "עובד", "salary", "payroll"],
            "שכירות": ["שכירות", "דמי שכירות", "שוכר", "rent"],
            "חשמל ומים": ["חשמל", "מים", "חברת חשמל", "מי", "ביוב", "electricity", "water"],
            "אינטרנט וטלפון": ["סלקום", "פרטנר", "הוט", "בזק", "אינטרנט", "סלולר", "cellcom", "partner", "hot", "bezeq"],
            "ייעוץ מקצועי": ["עורך דין", "רו״ח", "ייעוץ", "יועץ", "lawyer", "accountant", "consulting"],
            "ביטוח": ["ביטוח", "מגדל", "הפניקס", "כלל", "insurance", "migdal", "phoenix"],
            "ריהוט וציוד": ["ריהוט", "שולחן", "כסא", "ארון", "איקאה", "ikea", "furniture"],
            "תחזוקה ותיקונים": ["תיקון", "תחזוקה", "אחזקה", "שיפוץ", "repair", "maintenance"],
        }
        
        # Find matching category
        for category_name, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in vendor_lower:
                    category = db.query(Category).filter(
                        Category.name_hebrew == category_name
                    ).first()
                    if category:
                        return category.id
        
        return None  # Return None if no match (user will categorize manually)
    
    async def _check_duplicate(self, receipt: Receipt, db: Session) -> bool:
        """
        Check if receipt is a duplicate
        Matches by: vendor + date + amount (within 1 day and ±5%)
        
        Args:
            receipt: Receipt object
            db: Database session
            
        Returns:
            True if duplicate found, False otherwise
        """
        if not all([receipt.vendor_name, receipt.receipt_date, receipt.total_amount]):
            return False
        
        # Query similar receipts
        date_range_start = receipt.receipt_date - timedelta(days=1)
        date_range_end = receipt.receipt_date + timedelta(days=1)
        
        amount_tolerance = receipt.total_amount * 0.05  # 5% tolerance
        amount_min = receipt.total_amount - amount_tolerance
        amount_max = receipt.total_amount + amount_tolerance
        
        similar_receipts = db.query(Receipt).filter(
            Receipt.user_id == receipt.user_id,
            Receipt.id != receipt.id,
            Receipt.vendor_name == receipt.vendor_name,
            Receipt.receipt_date >= date_range_start,
            Receipt.receipt_date <= date_range_end,
            Receipt.total_amount >= amount_min,
            Receipt.total_amount <= amount_max,
            Receipt.status != ReceiptStatus.FAILED
        ).first()
        
        if similar_receipts:
            receipt.duplicate_of_id = similar_receipts.id
            logger.info(f"Duplicate detected: {receipt.id} is duplicate of {similar_receipts.id}")
            return True
        
        return False
    
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
