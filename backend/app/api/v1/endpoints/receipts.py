"""
Receipt endpoints
CRUD operations for receipts with secure file upload
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, BackgroundTasks, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from datetime import datetime
import logging

from app.core.dependencies import get_db, get_current_user, check_subscription_limit
from app.schemas.receipt import (
    ReceiptResponse, 
    ReceiptCreate, 
    ReceiptUpdate,
    ReceiptUploadResponse,
    ReceiptProcessingStatus,
    ReceiptDetail,
    ReceiptListItem,
    ReceiptListResponse,
    ReceiptApprove
)
from app.models.user import User
from app.models.receipt import Receipt, ReceiptStatus
from app.models.category import Category
from app.models.receipt_edit import ReceiptEdit
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


@router.get("/", response_model=ReceiptListResponse)
async def list_receipts(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    date_from: Optional[datetime] = Query(None, description="Filter by start date"),
    date_to: Optional[datetime] = Query(None, description="Filter by end date"),
    category_ids: Optional[str] = Query(None, description="Comma-separated category IDs"),
    amount_min: Optional[float] = Query(None, ge=0, description="Minimum amount"),
    amount_max: Optional[float] = Query(None, ge=0, description="Maximum amount"),
    status: Optional[ReceiptStatus] = Query(None, description="Filter by status"),
    search_query: Optional[str] = Query(None, description="Search in vendor/receipt number"),
    sort_by: str = Query(default="created_at", description="Sort field"),
    sort_order: str = Query(default="desc", description="Sort order (asc/desc)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List user's receipts with filtering, sorting, and pagination
    
    Filters:
    - date_from/date_to: Filter by receipt date range
    - category_ids: Filter by categories (comma-separated IDs)
    - amount_min/amount_max: Filter by amount range
    - status: Filter by processing status
    - search_query: Search in vendor name, receipt number, business number
    
    Sorting:
    - sort_by: created_at, receipt_date, total_amount, vendor_name
    - sort_order: asc, desc
    
    Returns:
        Paginated list of receipts with total count
    """
    # Base query - only user's receipts
    query = db.query(Receipt).filter(Receipt.user_id == current_user.id)
    
    # Apply date filters
    if date_from:
        query = query.filter(Receipt.receipt_date >= date_from)
    if date_to:
        query = query.filter(Receipt.receipt_date <= date_to)
    
    # Apply category filter
    if category_ids:
        try:
            cat_ids = [int(id.strip()) for id in category_ids.split(',')]
            query = query.filter(Receipt.category_id.in_(cat_ids))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="מזהי קטגוריות לא תקינים"
            )
    
    # Apply amount filters
    if amount_min is not None:
        query = query.filter(Receipt.total_amount >= amount_min)
    if amount_max is not None:
        query = query.filter(Receipt.total_amount <= amount_max)
    
    # Apply status filter
    if status:
        query = query.filter(Receipt.status == status)
    
    # Apply search query
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            or_(
                Receipt.vendor_name.ilike(search_term),
                Receipt.receipt_number.ilike(search_term),
                Receipt.business_number.ilike(search_term)
            )
        )
    
    # Count total before pagination
    total = query.count()
    
    # Apply sorting
    sort_column = getattr(Receipt, sort_by, Receipt.created_at)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Apply pagination
    offset = (page - 1) * page_size
    receipts = query.offset(offset).limit(page_size).all()
    
    # Build response with category names
    receipt_list = []
    for receipt in receipts:
        category_name = None
        if receipt.category_id:
            category = db.query(Category).filter(Category.id == receipt.category_id).first()
            if category:
                category_name = category.name_hebrew
        
        receipt_list.append(ReceiptListItem(
            id=receipt.id,
            vendor_name=receipt.vendor_name,
            receipt_date=receipt.receipt_date,
            total_amount=receipt.total_amount,
            category_name=category_name,
            status=receipt.status,
            is_duplicate=receipt.is_duplicate,
            created_at=receipt.created_at
        ))
    
    pages = (total + page_size - 1) // page_size
    
    logger.info(f"Listed {len(receipt_list)} receipts for user {current_user.id} (page {page}/{pages})")
    
    return ReceiptListResponse(
        receipts=receipt_list,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )


@router.get("/{receipt_id}", response_model=ReceiptDetail)
async def get_receipt(
    receipt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get single receipt details
    
    Returns full receipt data including category name
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
    
    # Get category name
    category_name = None
    if receipt.category_id:
        category = db.query(Category).filter(Category.id == receipt.category_id).first()
        if category:
            category_name = category.name_hebrew
    
    receipt_dict = {
        **receipt.__dict__,
        "category_name": category_name
    }
    
    logger.info(f"Retrieved receipt {receipt_id} for user {current_user.id}")
    
    return ReceiptDetail(**receipt_dict)


@router.put("/{receipt_id}", response_model=ReceiptDetail)
async def update_receipt(
    receipt_id: int,
    update_data: ReceiptUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update receipt data (during review process)
    
    Records edit history for all changes
    Can only edit receipts in REVIEW or DUPLICATE status
    Recalculates VAT if amounts changed
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
    
    # Can only edit receipts in REVIEW or DUPLICATE status
    if receipt.status not in [ReceiptStatus.REVIEW, ReceiptStatus.DUPLICATE]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="לא ניתן לערוך קבלה שאושרה או נכשלה"
        )
    
    # Track changes for edit history
    changes_made = False
    for field, new_value in update_data.dict(exclude_unset=True).items():
        if new_value is not None:
            old_value = getattr(receipt, field)
            if old_value != new_value:
                # Record edit
                edit = ReceiptEdit(
                    receipt_id=receipt.id,
                    user_id=current_user.id,
                    field_name=field,
                    old_value=str(old_value) if old_value else None,
                    new_value=str(new_value)
                )
                db.add(edit)
                
                # Update field
                setattr(receipt, field, new_value)
                changes_made = True
    
    # Recalculate VAT if amounts changed
    if any([update_data.total_amount, update_data.vat_amount, update_data.pre_vat_amount]):
        await receipt_service.recalculate_vat(receipt)
    
    if changes_made:
        receipt.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(receipt)
        logger.info(f"Receipt {receipt_id} updated by user {current_user.id}")
    
    return await get_receipt(receipt_id, current_user, db)


@router.post("/{receipt_id}/approve", response_model=ReceiptDetail)
async def approve_receipt(
    receipt_id: int,
    approve_data: ReceiptApprove,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Approve receipt (final submission)
    
    Validates all required fields are present
    Updates status to APPROVED
    Records approval timestamp
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
    
    if receipt.status != ReceiptStatus.REVIEW:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="לא ניתן לאשר קבלה שכבר אושרה"
        )
    
    # Update with approved data
    receipt.vendor_name = approve_data.vendor_name
    receipt.business_number = approve_data.business_number
    receipt.receipt_number = approve_data.receipt_number
    receipt.receipt_date = approve_data.receipt_date
    receipt.total_amount = approve_data.total_amount
    receipt.category_id = approve_data.category_id
    receipt.notes = approve_data.notes
    
    # Recalculate VAT
    await receipt_service.recalculate_vat(receipt)
    
    # Update status
    receipt.status = ReceiptStatus.APPROVED
    receipt.approved_at = datetime.utcnow()
    
    db.commit()
    db.refresh(receipt)
    
    logger.info(f"Receipt {receipt_id} approved by user {current_user.id}")
    
    return await get_receipt(receipt_id, current_user, db)


@router.delete("/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_receipt(
    receipt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete receipt
    
    Deletes file from S3 storage
    Removes from database (CASCADE will delete edits)
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
    
    # Delete file from S3
    await storage_service.delete_file(receipt.file_url)
    
    # Delete from database (CASCADE will delete edits)
    db.delete(receipt)
    db.commit()
    
    logger.info(f"Receipt {receipt_id} deleted by user {current_user.id}")
    
    return None


@router.post("/{receipt_id}/retry", status_code=status.HTTP_202_ACCEPTED)
async def retry_processing(
    receipt_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retry OCR processing for failed receipt
    
    Can only retry receipts in FAILED status
    Resets status to PROCESSING and triggers background job
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
    
    if receipt.status != ReceiptStatus.FAILED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ניתן לנסות שוב רק קבלות שנכשלו"
        )
    
    # Reset status
    receipt.status = ReceiptStatus.PROCESSING
    receipt.processing_started_at = datetime.utcnow()
    receipt.processing_completed_at = None
    db.commit()
    
    # Retry processing
    background_tasks.add_task(
        receipt_service.process_receipt,
        receipt.id,
        db
    )
    
    logger.info(f"Retrying processing for receipt {receipt_id}")
    
    return {"message": "מעבד מחדש את הקבלה"}

