"""
OCR Service
Google Cloud Vision API integration for Hebrew receipt text extraction
"""

from google.cloud import vision
from google.oauth2 import service_account
import os
import re
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import requests
from io import BytesIO

from ..core.config import settings

logger = logging.getLogger(__name__)


class OCRService:
    """OCR service using Google Cloud Vision API for Hebrew receipt processing"""
    
    def __init__(self):
        """Initialize Google Cloud Vision client with credentials"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_CLOUD_VISION_CREDENTIALS
            )
            self.client = vision.ImageAnnotatorClient(credentials=credentials)
            logger.info("Google Cloud Vision client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Vision client: {str(e)}")
            raise
    
    async def extract_text_from_url(self, image_url: str) -> Dict[str, Any]:
        """
        Extract text from receipt image using Google Cloud Vision
        Returns dictionary with extracted data and confidence scores
        
        Args:
            image_url: S3 URL to receipt image
            
        Returns:
            Dictionary with success status, full_text, parsed_data, and raw_response
        """
        try:
            logger.info(f"Starting OCR extraction for: {image_url}")
            
            # Download image from S3
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            image_content = response.content
            
            # Create Vision API image object
            image = vision.Image(content=image_content)
            
            # Perform document text detection (optimized for receipts and documents)
            response = self.client.document_text_detection(
                image=image,
                image_context={"language_hints": ["he", "en"]}  # Hebrew and English
            )
            
            if response.error.message:
                raise Exception(f"Vision API error: {response.error.message}")
            
            # Extract full text
            full_text = response.full_text_annotation.text if response.full_text_annotation else ""
            
            logger.info(f"OCR extracted {len(full_text)} characters")
            
            # Parse extracted text into structured data
            parsed_data = self._parse_receipt_text(full_text)
            
            return {
                "success": True,
                "full_text": full_text,
                "parsed_data": parsed_data,
                "raw_response": self._serialize_response(response)
            }
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "full_text": "",
                "parsed_data": {}
            }
    
    def _parse_receipt_text(self, text: str) -> Dict[str, Any]:
        """
        Parse receipt text and extract structured data
        Handles Hebrew and English text with Israeli receipt formats
        
        Args:
            text: Raw OCR text from receipt
            
        Returns:
            Dictionary with vendor, amounts, dates, etc. and confidence scores
        """
        parsed = {
            "vendor_name": None,
            "business_number": None,
            "receipt_number": None,
            "receipt_date": None,
            "total_amount": None,
            "vat_amount": None,
            "pre_vat_amount": None,
            "confidence": {
                "vendor_name": 0.0,
                "business_number": 0.0,
                "receipt_number": 0.0,
                "receipt_date": 0.0,
                "total_amount": 0.0,
                "vat_amount": 0.0
            }
        }
        
        lines = text.split('\n')
        
        # Extract vendor name (usually first non-empty line)
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if len(line) > 3 and not line.replace('.', '').replace(',', '').isdigit():
                parsed["vendor_name"] = line
                parsed["confidence"]["vendor_name"] = 0.85
                break
        
        # Extract business number (ח.פ / עוסק מורשה / ע.מ)
        business_patterns = [
            r'ח\.?פ\.?\s*:?\s*(\d{9})',
            r'עוסק מורשה\s*:?\s*(\d{9})',
            r'ע\.?מ\.?\s*:?\s*(\d{9})',
            r'business.*?(\d{9})',
            r'מס[\'׳]\s*עוסק\s*:?\s*(\d{9})',
        ]
        for pattern in business_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                parsed["business_number"] = match.group(1)
                parsed["confidence"]["business_number"] = 0.90
                break
        
        # Extract receipt number
        receipt_patterns = [
            r'קבלה\s*(?:מס\'|מספר|#)?\s*:?\s*(\d+)',
            r'receipt\s*(?:no|number|#)?\s*:?\s*(\d+)',
            r'מסמך\s*:?\s*(\d+)',
            r'חשבונית\s*(?:מס\'|מספר)?\s*:?\s*(\d+)',
        ]
        for pattern in receipt_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                parsed["receipt_number"] = match.group(1)
                parsed["confidence"]["receipt_number"] = 0.85
                break
        
        # Extract date - multiple formats (DD/MM/YYYY, DD.MM.YYYY, etc.)
        date_patterns = [
            r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})',  # DD/MM/YYYY
            r'(\d{2,4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})',  # YYYY/MM/DD
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    groups = match.groups()
                    # Determine format based on first group length
                    if len(groups[0]) == 4:  # YYYY/MM/DD
                        year, month, day = groups
                    else:  # DD/MM/YYYY
                        day, month, year = groups
                    
                    if len(year) == 2:
                        year = f"20{year}"
                    
                    # Validate date ranges
                    day_int = int(day)
                    month_int = int(month)
                    year_int = int(year)
                    
                    if 1 <= day_int <= 31 and 1 <= month_int <= 12 and 2000 <= year_int <= 2030:
                        parsed["receipt_date"] = f"{year_int}-{month_int:02d}-{day_int:02d}"
                        parsed["confidence"]["receipt_date"] = 0.80
                        break
                except:
                    continue
        
        # Extract amounts (looking for "סה״כ", "total", amounts with ₪)
        amount_patterns = [
            r'סה[״\"]כ\s*:?\s*₪?\s*([\d,]+\.?\d{0,2})',
            r'total\s*:?\s*₪?\s*([\d,]+\.?\d{0,2})',
            r'לתשלום\s*:?\s*₪?\s*([\d,]+\.?\d{0,2})',
            r'סכום\s*כולל\s*:?\s*₪?\s*([\d,]+\.?\d{0,2})',
            r'₪\s*([\d,]+\.?\d{2})',
        ]
        amounts_found = []
        for pattern in amount_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    amount = float(match.replace(',', ''))
                    if 1 <= amount <= 100000:  # Reasonable range for receipts
                        amounts_found.append(amount)
                except:
                    continue
        
        if amounts_found:
            # Assume largest amount is total
            parsed["total_amount"] = max(amounts_found)
            parsed["confidence"]["total_amount"] = 0.80
        
        # Extract VAT (מע״מ)
        vat_patterns = [
            r'מע[״\"]מ\s*:?\s*₪?\s*([\d,]+\.?\d{0,2})',
            r'vat\s*:?\s*₪?\s*([\d,]+\.?\d{0,2})',
            r'מס\s*ערך\s*מוסף\s*:?\s*₪?\s*([\d,]+\.?\d{0,2})',
        ]
        for pattern in vat_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    parsed["vat_amount"] = float(match.group(1).replace(',', ''))
                    parsed["confidence"]["vat_amount"] = 0.85
                    break
                except:
                    continue
        
        # Calculate pre-VAT if we have total and VAT
        if parsed["total_amount"] and parsed["vat_amount"]:
            parsed["pre_vat_amount"] = round(parsed["total_amount"] - parsed["vat_amount"], 2)
        elif parsed["total_amount"]:
            # Assume 17% VAT (Israeli standard)
            parsed["vat_amount"] = round(parsed["total_amount"] * 0.17 / 1.17, 2)
            parsed["pre_vat_amount"] = round(parsed["total_amount"] - parsed["vat_amount"], 2)
            parsed["confidence"]["vat_amount"] = 0.70
        
        return parsed
    
    def _serialize_response(self, response) -> dict:
        """Convert Vision API response to JSON-serializable dict"""
        return {
            "text": response.full_text_annotation.text if response.full_text_annotation else "",
            "pages": len(response.full_text_annotation.pages) if response.full_text_annotation else 0
        }
    
    async def retry_extraction(self, image_url: str, attempt: int = 1) -> Dict[str, Any]:
        """
        Retry OCR extraction with exponential backoff
        
        Args:
            image_url: S3 URL to receipt image
            attempt: Starting attempt number (default 1)
            
        Returns:
            OCR extraction result
        """
        max_attempts = 3
        
        for i in range(attempt, max_attempts + 1):
            result = await self.extract_text_from_url(image_url)
            
            if result["success"]:
                logger.info(f"OCR succeeded on attempt {i}")
                return result
            
            if i < max_attempts:
                import asyncio
                wait_time = 2 ** i  # Exponential backoff: 2, 4, 8 seconds
                logger.info(f"Retrying OCR in {wait_time} seconds (attempt {i+1}/{max_attempts})")
                await asyncio.sleep(wait_time)
        
        logger.error(f"OCR failed after {max_attempts} attempts")
        return result  # Return last result even if failed


# Global OCR service instance
ocr_service = OCRService()
