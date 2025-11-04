"""
Hebrew translations for field names in edit history
Provides user-friendly Hebrew names for database fields
"""

from typing import Dict

# Hebrew translations for receipt fields
FIELD_NAMES_HE: Dict[str, str] = {
    'vendor_name': 'שם הספק',
    'business_number': 'מספר עוסק',
    'receipt_number': 'מספר קבלה',
    'receipt_date': 'תאריך',
    'total_amount': 'סכום כולל',
    'vat_amount': 'מע"מ',
    'pre_vat_amount': 'לפני מע"מ',
    'category_id': 'קטגוריה',
    'notes': 'הערות',
    'status': 'סטטוס',
    'is_verified': 'מאומת',
    'confidence_score': 'ציון אמינות'
}


def get_field_name_hebrew(field_name: str) -> str:
    """
    Get Hebrew translation of field name
    
    Args:
        field_name: English field name (e.g., 'vendor_name')
        
    Returns:
        Hebrew translation if exists, otherwise original field name
    """
    return FIELD_NAMES_HE.get(field_name, field_name)


def get_all_field_names() -> Dict[str, str]:
    """
    Get all field name translations
    
    Returns:
        Dictionary mapping English to Hebrew field names
    """
    return FIELD_NAMES_HE.copy()
