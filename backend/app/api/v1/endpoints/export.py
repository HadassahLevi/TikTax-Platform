"""
Export Endpoints
Generate and download Excel/CSV exports of receipt data
Includes secure temporary download URLs with expiration
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import uuid
import logging
import csv
import io

from app.db.session import get_db
from app.models.user import User
from app.models.receipt import Receipt, ReceiptStatus
from app.models.category import Category
from app.schemas.export import ExportRequest, ExportResponse, ExportFormat
from app.core.dependencies import get_current_user
from app.services.excel_service import excel_service
from app.utils.formatters import format_israeli_date

router = APIRouter()
logger = logging.getLogger(__name__)

# In-memory export storage (Production: use Redis or S3 with presigned URLs)
export_storage = {}


@router.post("/generate", response_model=ExportResponse, status_code=status.HTTP_201_CREATED)
async def generate_export(
    request: ExportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate export file (Excel/CSV)
    
    Returns download URL that expires in 1 hour.
    Only includes APPROVED receipts.
    
    **Request Body:**
    - format: "excel" or "csv" (PDF coming soon)
    - date_from: Start date (inclusive)
    - date_to: End date (inclusive)
    - category_ids: Optional list of category IDs to filter
    - include_images: Include receipt images (not implemented yet)
    
    **Response:**
    - export_id: Unique identifier for download
    - download_url: URL to download the file
    - expires_at: Expiration timestamp (1 hour)
    - file_size: File size in bytes
    - message: Success message in Hebrew
    """
    # Validate date range
    if request.date_from > request.date_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="תאריך התחלה חייב להיות לפני תאריך הסיום"
        )
    
    # Check date range is not too large (prevent abuse)
    date_diff = (request.date_to - request.date_from).days
    if date_diff > 730:  # 2 years max
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="טווח תאריכים מקסימלי: שנתיים"
        )
    
    # Query receipts (only APPROVED)
    query = db.query(Receipt).filter(
        Receipt.user_id == current_user.id,
        Receipt.receipt_date >= request.date_from,
        Receipt.receipt_date <= request.date_to,
        Receipt.status == ReceiptStatus.APPROVED
    )
    
    # Filter by categories if specified
    if request.category_ids:
        query = query.filter(Receipt.category_id.in_(request.category_ids))
    
    receipts = query.order_by(Receipt.receipt_date.asc()).all()
    
    if not receipts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="לא נמצאו קבלות בתקופה המבוקשת"
        )
    
    # Get all categories for lookup
    categories = db.query(Category).all()
    
    # Generate export based on format
    try:
        if request.format == ExportFormat.EXCEL:
            file_content = excel_service.generate_export(
                current_user,
                receipts,
                categories,
                request.date_from,
                request.date_to
            )
            filename = f"tiktax_receipts_{request.date_from.strftime('%Y%m%d')}_{request.date_to.strftime('%Y%m%d')}.xlsx"
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        
        elif request.format == ExportFormat.PDF:
            # PDF generation (to be implemented)
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="ייצוא PDF יהיה זמין בקרוב"
            )
        
        elif request.format == ExportFormat.CSV:
            # CSV generation
            file_content = _generate_csv(receipts, categories)
            filename = f"tiktax_receipts_{request.date_from.strftime('%Y%m%d')}_{request.date_to.strftime('%Y%m%d')}.csv"
            mime_type = "text/csv; charset=utf-8"
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="פורמט לא נתמך"
            )
        
        # Generate export ID and store
        export_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        export_storage[export_id] = {
            'content': file_content,
            'filename': filename,
            'mime_type': mime_type,
            'expires_at': expires_at,
            'user_id': current_user.id
        }
        
        download_url = f"/api/v1/export/download/{export_id}"
        
        logger.info(
            f"Export generated: {export_id} | User: {current_user.id} | "
            f"Format: {request.format} | Receipts: {len(receipts)} | Size: {len(file_content)} bytes"
        )
        
        return ExportResponse(
            export_id=export_id,
            download_url=download_url,
            expires_at=expires_at,
            file_size=len(file_content),
            message=f"הקובץ הופק בהצלחה - {len(receipts)} קבלות"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Export generation failed for user {current_user.id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="שגיאה ביצירת הקובץ. נסה שוב מאוחר יותר."
        )


@router.get("/download/{export_id}")
async def download_export(
    export_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Download generated export file
    
    **Path Parameters:**
    - export_id: Unique export identifier from generate endpoint
    
    **Security:**
    - Must be authenticated
    - Can only download own exports
    - Link expires after 1 hour
    
    **Returns:**
    - File download with appropriate headers
    """
    export_data = export_storage.get(export_id)
    
    if not export_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="קובץ לא נמצא או פג תוקפו"
        )
    
    # Verify ownership
    if export_data['user_id'] != current_user.id:
        logger.warning(
            f"Unauthorized export download attempt: Export {export_id} | "
            f"Owner: {export_data['user_id']} | Requester: {current_user.id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="אין הרשאה להוריד קובץ זה"
        )
    
    # Check expiration
    if datetime.utcnow() > export_data['expires_at']:
        # Clean up expired export
        del export_storage[export_id]
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="פג תוקף הקובץ. צור אותו מחדש."
        )
    
    logger.info(f"Export downloaded: {export_id} by user {current_user.id}")
    
    # Return file with proper headers
    return Response(
        content=export_data['content'],
        media_type=export_data['mime_type'],
        headers={
            'Content-Disposition': f'attachment; filename="{export_data["filename"]}"',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    )


@router.delete("/cleanup")
async def cleanup_expired_exports(
    current_user: User = Depends(get_current_user)
):
    """
    Cleanup expired exports (Admin/background task)
    
    This endpoint can be called periodically to free memory.
    In production, use a scheduled job or Redis with TTL.
    """
    now = datetime.utcnow()
    expired_ids = [
        export_id for export_id, data in export_storage.items()
        if data['expires_at'] <= now
    ]
    
    for export_id in expired_ids:
        del export_storage[export_id]
    
    logger.info(f"Cleaned up {len(expired_ids)} expired exports")
    
    return {
        "message": f"נוקו {len(expired_ids)} קבצים שפג תוקפם",
        "cleaned_count": len(expired_ids),
        "remaining_count": len(export_storage)
    }


def _generate_csv(receipts: List[Receipt], categories: List[Category]) -> bytes:
    """
    Generate CSV export with Hebrew support
    
    Uses UTF-8 with BOM for proper Excel Hebrew display
    
    Args:
        receipts: List of receipts to export
        categories: All categories for lookup
        
    Returns:
        CSV file as bytes
    """
    output = io.StringIO()
    # Add BOM for Excel Hebrew support
    output.write('\ufeff')
    
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        "תאריך", "ספק", "מספר עוסק", "מספר קבלה",
        "קטגוריה", "לפני מע\"מ", "מע\"מ", "סה\"כ", "הערות"
    ])
    
    # Category lookup
    category_dict = {cat.id: cat.name_hebrew for cat in categories}
    
    # Data rows
    for receipt in receipts:
        writer.writerow([
            format_israeli_date(receipt.receipt_date) if receipt.receipt_date else "",
            receipt.vendor_name or "",
            receipt.business_number or "",
            receipt.receipt_number or "",
            category_dict.get(receipt.category_id, "לא מסווג"),
            f"{receipt.pre_vat_amount:.2f}" if receipt.pre_vat_amount else "0.00",
            f"{receipt.vat_amount:.2f}" if receipt.vat_amount else "0.00",
            f"{receipt.total_amount:.2f}" if receipt.total_amount else "0.00",
            receipt.notes or ""
        ])
    
    return output.getvalue().encode('utf-8-sig')

