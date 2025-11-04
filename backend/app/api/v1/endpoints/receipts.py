"""
Receipt endpoints
CRUD operations for receipts with secure file upload
"""

from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.core.dependencies import get_db, get_current_user, check_subscription_limit
from app.schemas.receipt import (
    ReceiptResponse, 
    ReceiptCreate, 
    ReceiptUpdate,
    ReceiptUploadResponse,
    ReceiptProcessingStatus
)
from app.models.user import User
from app.models.receipt import Receipt, ReceiptStatus
from app.services.storage_service import storage_service
from app.services.ocr_service import ocr_service
from app.services.receipt_service import receipt_service

router = APIRouter()
logger = logging.getLogger(__name__)

# File validation constants
ALLOWED_MIME_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/heic', 'image/heif']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MIN_FILE_SIZE = 10 * 1024  # 10 KB


@router.post("/upload", response_model=ReceiptUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_receipt(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload receipt image for processing
    - Validates file type and size
    - Uploads to S3 with optimization
    - Triggers OCR processing in background
    
    Returns:
        ReceiptUploadResponse with receipt_id and processing status
    """
    # Check subscription limit
    check_subscription_limit(current_user, db)
    
    # Validate file type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"סוג קובץ לא נתמך. נתמכים: JPEG, PNG, HEIC"
        )
    
    # Read file content
    file_content = await file.read()
    file_size = len(file_content)
    
    # Validate file size
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"קובץ גדול מדי. מקסימום: 10MB"
        )
    
    if file_size < MIN_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"קובץ קטן מדי. מינימום: 10KB"
        )
    
    try:
        # Upload to S3
        s3_url, optimized_size = await storage_service.upload_file(
            file_content=file_content,
            filename=file.filename,
            user_id=current_user.id,
            mime_type=file.content_type
        )
        
        # Create receipt record
        receipt = Receipt(
            user_id=current_user.id,
            original_filename=file.filename,
            file_url=s3_url,
            file_size=optimized_size,
            mime_type='image/jpeg',  # Always JPEG after optimization
            status=ReceiptStatus.PROCESSING,
            processing_started_at=datetime.utcnow()
        )
        
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        
        # Increment usage counter
        current_user.receipts_used_this_month += 1
        db.commit()
        
        logger.info(f"Receipt uploaded: {receipt.id} by user {current_user.id}")
        
        # Start OCR processing in background
        background_tasks.add_task(
            receipt_service.process_receipt,
            receipt.id,
            db
        )
        
        return ReceiptUploadResponse(
            receipt_id=receipt.id,
            status=ReceiptStatus.PROCESSING,
            message="הקבלה הועלתה בהצלחה ונמצאת בעיבוד"
        )
        
    except Exception as e:
        logger.error(f"Upload failed for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="העלאת הקבלה נכשלה. נסה שוב."
        )


@router.get("/{receipt_id}/status", response_model=ReceiptProcessingStatus)
async def get_processing_status(
    receipt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check receipt processing status
    Used for polling during OCR processing
    
    Args:
        receipt_id: Receipt ID to check
        
    Returns:
        ReceiptProcessingStatus with progress and OCR data
    """
    receipt = db.query(Receipt).filter(
        Receipt.id == receipt_id,
        Receipt.user_id == current_user.id
    ).first()
    
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="קבלה לא נמצאה"
        )
    
    # Calculate progress based on status
    progress_map = {
        ReceiptStatus.PROCESSING: 50,
        ReceiptStatus.REVIEW: 80,
        ReceiptStatus.APPROVED: 100,
        ReceiptStatus.FAILED: 0,
        ReceiptStatus.DUPLICATE: 100
    }
    
    message_map = {
        ReceiptStatus.PROCESSING: "מעבד את הקבלה...",
        ReceiptStatus.REVIEW: "הקבלה מוכנה לבדיקה",
        ReceiptStatus.APPROVED: "הקבלה אושרה",
        ReceiptStatus.FAILED: "עיבוד נכשל",
        ReceiptStatus.DUPLICATE: "זוהתה קבלה כפולה"
    }
    
    return ReceiptProcessingStatus(
        receipt_id=receipt.id,
        status=receipt.status,
        progress=progress_map.get(receipt.status, 0),
        message=message_map.get(receipt.status, "מעבד..."),
        ocr_data=receipt.ocr_data if receipt.status == ReceiptStatus.REVIEW else None
    )


@router.get("/", response_model=List[ReceiptResponse])
async def get_receipts(
    skip: int = 0,
    limit: int = 50,
    category_id: str = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's receipts with filtering and pagination
    """
    # TODO: Implement receipt listing with filters
    pass


@router.get("/{receipt_id}", response_model=ReceiptResponse)
async def get_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get single receipt by ID
    """
    # TODO: Implement get receipt
    pass


@router.put("/{receipt_id}", response_model=ReceiptResponse)
async def update_receipt(
    receipt_id: int,
    receipt_data: ReceiptUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update receipt details
    Tracks edit history
    """
    # TODO: Implement receipt update
    pass


@router.delete("/{receipt_id}", status_code=204)
async def delete_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Soft delete receipt
    """
    # TODO: Implement receipt deletion
    pass
