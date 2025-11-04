"""
PDF Export Service
Professional PDF report generation with Hebrew support and receipt images
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from typing import List, Optional
import io
import requests
from PIL import Image as PILImage
import logging

from ..models.receipt import Receipt
from ..models.category import Category
from ..models.user import User
from ..utils.formatters import format_amount, format_israeli_date

logger = logging.getLogger(__name__)


class PDFService:
    """
    Generate professional PDF reports for tax purposes.
    
    Features:
    - Title page with business info
    - Summary section with totals
    - Category breakdown table
    - Detailed receipts table (paginated)
    - Optional receipt images (one per page)
    - Page numbers on all pages
    - RTL Hebrew support
    """
    
    def __init__(self):
        """Initialize PDF service with Hebrew-compatible styles"""
        # Note: For full Hebrew support, download a Hebrew TTF font
        # and register it with: pdfmetrics.registerFont(TTFont('Hebrew', 'path/to/font.ttf'))
        # For now, we use Helvetica which has limited Hebrew support
        
        self.styles = getSampleStyleSheet()
        
        # Create RTL Hebrew style
        self.hebrew_style = ParagraphStyle(
            'Hebrew',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            alignment=TA_RIGHT,
            wordWrap='RTL'
        )
        
        self.hebrew_title = ParagraphStyle(
            'HebrewTitle',
            parent=self.styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=18,
            alignment=TA_CENTER
        )
    
    def generate_export(
        self,
        user: User,
        receipts: List[Receipt],
        categories: List[Category],
        date_from: datetime,
        date_to: datetime,
        include_images: bool = False
    ) -> bytes:
        """
        Generate professional PDF report
        
        Args:
            user: User requesting the export
            receipts: List of receipts to include
            categories: List of all categories for lookup
            date_from: Report start date
            date_to: Report end date
            include_images: Whether to include receipt images
            
        Returns:
            PDF file as bytes
        """
        logger.info(
            f"Generating PDF export for user {user.id}: "
            f"{len(receipts)} receipts, images={include_images}"
        )
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )
        
        story = []
        
        # Title page
        story.extend(self._create_title_page(user, date_from, date_to))
        story.append(PageBreak())
        
        # Summary section
        story.extend(self._create_summary_section(receipts))
        story.append(Spacer(1, 10*mm))
        
        # Category breakdown
        story.extend(self._create_category_section(receipts, categories))
        story.append(PageBreak())
        
        # Detailed receipts table
        story.extend(self._create_details_section(receipts, categories))
        
        # Receipt images (if requested)
        if include_images and receipts:
            logger.info(f"Adding {len(receipts)} receipt images to PDF")
            story.append(PageBreak())
            story.extend(self._create_images_section(receipts))
        
        # Build PDF with page numbers
        try:
            doc.build(story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)
            logger.info(f"PDF generated successfully: {buffer.tell()} bytes")
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}", exc_info=True)
            raise
        
        buffer.seek(0)
        return buffer.read()
    
    def _create_title_page(self, user: User, date_from: datetime, date_to: datetime):
        """Create title page with business information"""
        elements = []
        
        # Title
        title = Paragraph("דוח קבלות", self.hebrew_title)
        elements.append(title)
        elements.append(Spacer(1, 10*mm))
        
        # Business info table
        data = [
            ["שם העסק:", user.business_name or "לא צוין"],
            ["מספר עוסק:", user.business_number or "לא צוין"],
            ["תקופת הדוח:", f"{format_israeli_date(date_from)} - {format_israeli_date(date_to)}"],
            ["תאריך יצירה:", format_israeli_date(datetime.utcnow())]
        ]
        
        table = Table(data, colWidths=[50*mm, 100*mm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_summary_section(self, receipts: List[Receipt]):
        """Create summary section with totals"""
        elements = []
        
        # Section title
        title = Paragraph("סיכום", self.hebrew_title)
        elements.append(title)
        elements.append(Spacer(1, 5*mm))
        
        # Calculate totals
        total_receipts = len(receipts)
        total_amount = sum([r.total_amount or 0 for r in receipts])
        total_vat = sum([r.vat_amount or 0 for r in receipts])
        total_pre_vat = sum([r.pre_vat_amount or 0 for r in receipts])
        
        # Summary table
        data = [
            ["סה\"כ קבלות:", str(total_receipts)],
            ["סה\"כ לפני מע\"מ:", f"₪{format_amount(total_pre_vat)}"],
            ["סה\"כ מע\"מ:", f"₪{format_amount(total_vat)}"],
            ["סה\"כ כולל מע\"מ:", f"₪{format_amount(total_amount)}"]
        ]
        
        table = Table(data, colWidths=[60*mm, 60*mm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 3), (-1, 3), colors.lightgreen),
            ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_category_section(self, receipts: List[Receipt], categories: List[Category]):
        """Create category breakdown section"""
        elements = []
        
        # Section title
        title = Paragraph("פירוט לפי קטגוריה", self.hebrew_title)
        elements.append(title)
        elements.append(Spacer(1, 5*mm))
        
        # Group by category
        from collections import defaultdict
        category_data = defaultdict(lambda: {'count': 0, 'total': 0.0})
        
        for receipt in receipts:
            if receipt.category_id and receipt.total_amount:
                category_data[receipt.category_id]['count'] += 1
                category_data[receipt.category_id]['total'] += receipt.total_amount
        
        # Category lookup
        category_dict = {cat.id: cat.name_hebrew for cat in categories}
        
        # Calculate grand total
        grand_total = sum([data['total'] for data in category_data.values()])
        
        # Create table data
        table_data = [["קטגוריה", "מספר קבלות", "סכום כולל", "אחוז"]]
        
        for cat_id, data in sorted(category_data.items(), key=lambda x: x[1]['total'], reverse=True):
            percentage = (data['total'] / grand_total * 100) if grand_total > 0 else 0
            table_data.append([
                category_dict.get(cat_id, "לא מסווג"),
                str(data['count']),
                f"₪{format_amount(data['total'])}",
                f"{percentage:.1f}%"
            ])
        
        # Total row
        table_data.append([
            "סה\"כ",
            str(len(receipts)),
            f"₪{format_amount(grand_total)}",
            "100%"
        ])
        
        table = Table(table_data, colWidths=[50*mm, 30*mm, 35*mm, 25*mm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_details_section(self, receipts: List[Receipt], categories: List[Category]):
        """Create detailed receipts table"""
        elements = []
        
        # Section title
        title = Paragraph("פירוט קבלות", self.hebrew_title)
        elements.append(title)
        elements.append(Spacer(1, 5*mm))
        
        # Category lookup
        category_dict = {cat.id: cat.name_hebrew for cat in categories}
        
        # Table header
        table_data = [[
            "תאריך", "ספק", "קטגוריה",
            "לפני מע\"מ", "מע\"מ", "סה\"כ"
        ]]
        
        # Data rows (split into chunks if too many)
        chunk_size = 30  # Receipts per page
        for i, receipt in enumerate(receipts):
            if i > 0 and i % chunk_size == 0:
                # Create table for current chunk
                table = self._create_receipts_table(table_data)
                elements.append(table)
                elements.append(PageBreak())
                
                # Reset for next chunk
                table_data = [[
                    "תאריך", "ספק", "קטגוריה",
                    "לפני מע\"מ", "מע\"מ", "סה\"כ"
                ]]
            
            table_data.append([
                format_israeli_date(receipt.receipt_date) if receipt.receipt_date else "",
                receipt.vendor_name or "",
                category_dict.get(receipt.category_id, ""),
                f"₪{format_amount(receipt.pre_vat_amount)}",
                f"₪{format_amount(receipt.vat_amount)}",
                f"₪{format_amount(receipt.total_amount)}"
            ])
        
        # Add final table
        if len(table_data) > 1:
            table = self._create_receipts_table(table_data)
            elements.append(table)
        
        return elements
    
    def _create_receipts_table(self, data):
        """Helper to create styled receipts table"""
        table = Table(data, colWidths=[25*mm, 45*mm, 30*mm, 25*mm, 20*mm, 25*mm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3F4F6')]),
        ]))
        return table
    
    def _create_images_section(self, receipts: List[Receipt]):
        """Create section with receipt images (one per page)"""
        elements = []
        
        for i, receipt in enumerate(receipts):
            # Title
            title_text = f"קבלה: {receipt.vendor_name or 'לא ידוע'} - {format_israeli_date(receipt.receipt_date) if receipt.receipt_date else ''}"
            title = Paragraph(title_text, self.hebrew_style)
            elements.append(title)
            elements.append(Spacer(1, 5*mm))
            
            try:
                # Download image
                logger.info(f"Downloading receipt image {i+1}/{len(receipts)}: {receipt.file_url}")
                response = requests.get(receipt.file_url, timeout=10)
                response.raise_for_status()
                
                img_data = io.BytesIO(response.content)
                
                # Load and resize image to fit page
                pil_img = PILImage.open(img_data)
                max_width = 170*mm
                max_height = 220*mm
                
                # Calculate scaling
                width_scale = max_width / pil_img.width
                height_scale = max_height / pil_img.height
                scale = min(width_scale, height_scale)
                
                new_width = pil_img.width * scale
                new_height = pil_img.height * scale
                
                # Reset image data for ReportLab
                img_data.seek(0)
                
                # Create ReportLab image
                img = Image(img_data, width=new_width, height=new_height)
                elements.append(img)
                
                logger.info(f"Receipt image {i+1} added successfully")
                
            except requests.RequestException as e:
                error_text = Paragraph(f"שגיאה בטעינת תמונה: בעיית רשת - {str(e)}", self.hebrew_style)
                elements.append(error_text)
                logger.warning(f"Failed to download receipt image {i+1}: {str(e)}")
                
            except Exception as e:
                error_text = Paragraph(f"שגיאה בטעינת תמונה: {str(e)}", self.hebrew_style)
                elements.append(error_text)
                logger.error(f"Failed to process receipt image {i+1}: {str(e)}", exc_info=True)
            
            # Page break after each image (except last)
            if i < len(receipts) - 1:
                elements.append(PageBreak())
        
        return elements
    
    def _add_page_number(self, canvas, doc):
        """Add page number to footer"""
        page_num = canvas.getPageNumber()
        text = f"עמוד {page_num}"
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(200*mm, 10*mm, text)
        canvas.restoreState()


# Singleton instance
pdf_service = PDFService()
