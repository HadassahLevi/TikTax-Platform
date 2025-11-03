"""
Export endpoints
Generate Excel and PDF exports
"""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user

router = APIRouter()


@router.get("/excel")
async def export_to_excel(
    start_date: str = Query(...),
    end_date: str = Query(...),
    category_ids: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Export receipts to Excel (accountant-ready format)
    """
    # TODO: Implement Excel export
    pass


@router.get("/pdf/{receipt_id}")
async def export_receipt_to_pdf(
    receipt_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Export single receipt to PDF
    """
    # TODO: Implement PDF export
    pass
