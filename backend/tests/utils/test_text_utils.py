"""
Unit tests for text utilities
Testing Hebrew text normalization and similarity functions
"""

import pytest
from app.utils.text_utils import (
    normalize_hebrew_text,
    clean_business_number,
    extract_numbers_from_text,
    is_hebrew,
    truncate_with_ellipsis,
    sanitize_filename,
    highlight_search_term
)


class TestNormalizeHebrewText:
    """Tests for Hebrew text normalization"""
    
    def test_normalize_basic_hebrew(self):
        """Test basic Hebrew text normalization"""
        text = "שלום עולם"
        result = normalize_hebrew_text(text)
        assert result == "שלום עולם"
    
    def test_normalize_with_nikud(self):
        """Test removal of Hebrew diacritics (nikud)"""
        text = "שָׁלוֹם עוֹלָם"
        result = normalize_hebrew_text(text)
        assert result == "שלום עולם"
    
    def test_normalize_with_special_chars(self):
        """Test removal of special characters"""
        text = "שלום! עולם?"
        result = normalize_hebrew_text(text)
        assert result == "שלום עולם"
    
    def test_normalize_with_numbers(self):
        """Test preservation of numbers"""
        text = "קבלה 123"
        result = normalize_hebrew_text(text)
        assert "123" in result
    
    def test_normalize_mixed_hebrew_english(self):
        """Test mixed Hebrew and English"""
        text = "Super סופר"
        result = normalize_hebrew_text(text)
        assert "super" in result
        assert "סופר" in result
    
    def test_normalize_whitespace(self):
        """Test whitespace normalization"""
        text = "שלום    עולם   "
        result = normalize_hebrew_text(text)
        assert result == "שלום עולם"
    
    def test_normalize_empty_string(self):
        """Test empty string"""
        assert normalize_hebrew_text("") == ""
    
    def test_normalize_none(self):
        """Test None input"""
        assert normalize_hebrew_text(None) == ""


class TestCleanBusinessNumber:
    """Tests for business number cleaning"""
    
    def test_clean_valid_number(self):
        """Test valid 9-digit number"""
        assert clean_business_number("123456789") == "123456789"
    
    def test_clean_with_dashes(self):
        """Test number with dashes"""
        assert clean_business_number("12-345-6789") == "123456789"
    
    def test_clean_short_number(self):
        """Test padding short numbers"""
        assert clean_business_number("12345") == "000012345"
    
    def test_clean_with_spaces(self):
        """Test number with spaces"""
        assert clean_business_number("123 456 789") == "123456789"
    
    def test_clean_empty_string(self):
        """Test empty string"""
        assert clean_business_number("") == ""
    
    def test_clean_none(self):
        """Test None input"""
        assert clean_business_number(None) == ""


class TestExtractNumbersFromText:
    """Tests for number extraction"""
    
    def test_extract_single_number(self):
        """Test extracting single number"""
        result = extract_numbers_from_text("קבלה 123")
        assert result == ["123"]
    
    def test_extract_multiple_numbers(self):
        """Test extracting multiple numbers"""
        result = extract_numbers_from_text("קבלה 123 סכום 456")
        assert result == ["123", "456"]
    
    def test_extract_from_mixed_text(self):
        """Test extraction from mixed Hebrew-English text"""
        result = extract_numbers_from_text("Receipt #12345 סכום ₪99.50")
        assert "12345" in result
        assert "99" in result
        assert "50" in result
    
    def test_extract_no_numbers(self):
        """Test text with no numbers"""
        result = extract_numbers_from_text("שלום עולם")
        assert result == []
    
    def test_extract_empty_string(self):
        """Test empty string"""
        assert extract_numbers_from_text("") == []


class TestIsHebrew:
    """Tests for Hebrew detection"""
    
    def test_pure_hebrew(self):
        """Test pure Hebrew text"""
        assert is_hebrew("שלום עולם") is True
    
    def test_mixed_text(self):
        """Test mixed Hebrew-English"""
        assert is_hebrew("Hello שלום") is True
    
    def test_english_only(self):
        """Test English only"""
        assert is_hebrew("Hello World") is False
    
    def test_numbers_only(self):
        """Test numbers only"""
        assert is_hebrew("123456") is False
    
    def test_empty_string(self):
        """Test empty string"""
        assert is_hebrew("") is False
    
    def test_hebrew_with_nikud(self):
        """Test Hebrew with diacritics"""
        assert is_hebrew("שָׁלוֹם") is True


class TestTruncateWithEllipsis:
    """Tests for text truncation"""
    
    def test_short_text(self):
        """Test text shorter than max length"""
        text = "שלום"
        result = truncate_with_ellipsis(text, 20)
        assert result == "שלום"
    
    def test_exact_length(self):
        """Test text at exact max length"""
        text = "a" * 50
        result = truncate_with_ellipsis(text, 50)
        assert result == text
    
    def test_long_text(self):
        """Test text longer than max length"""
        text = "a" * 100
        result = truncate_with_ellipsis(text, 50)
        assert len(result) == 50
        assert result.endswith("...")
    
    def test_hebrew_truncation(self):
        """Test Hebrew text truncation"""
        text = "שלום עולם " * 10
        result = truncate_with_ellipsis(text, 30)
        assert len(result) == 30
        assert result.endswith("...")
    
    def test_empty_string(self):
        """Test empty string"""
        assert truncate_with_ellipsis("", 50) == ""


class TestSanitizeFilename:
    """Tests for filename sanitization"""
    
    def test_simple_filename(self):
        """Test simple filename"""
        assert sanitize_filename("receipt.jpg") == "receipt.jpg"
    
    def test_filename_with_spaces(self):
        """Test filename with spaces"""
        result = sanitize_filename("my receipt.jpg")
        assert result == "my_receipt.jpg"
    
    def test_filename_with_path(self):
        """Test filename with path separators"""
        result = sanitize_filename("path/to/file.jpg")
        assert "/" not in result
        assert result == "path_to_file.jpg"
    
    def test_hebrew_filename(self):
        """Test Hebrew filename"""
        result = sanitize_filename("קבלה.jpg")
        assert ".jpg" in result
    
    def test_long_filename(self):
        """Test very long filename"""
        long_name = "a" * 100 + ".jpg"
        result = sanitize_filename(long_name)
        assert len(result) <= 55  # 50 + .jpg
    
    def test_empty_filename(self):
        """Test empty filename"""
        assert sanitize_filename("") == "unnamed"
    
    def test_none_filename(self):
        """Test None filename"""
        assert sanitize_filename(None) == "unnamed"


class TestHighlightSearchTerm:
    """Tests for search term highlighting"""
    
    def test_term_in_middle(self):
        """Test term in middle of text"""
        text = "This is a test sentence with some words"
        result = highlight_search_term(text, "test", 50)
        assert "test" in result
    
    def test_term_at_start(self):
        """Test term at start of text"""
        text = "Test is at the beginning"
        result = highlight_search_term(text, "Test", 50)
        assert result.startswith("Test")
    
    def test_term_at_end(self):
        """Test term at end of text"""
        text = "The word is at the end test"
        result = highlight_search_term(text, "test", 50)
        assert "test" in result
    
    def test_hebrew_term(self):
        """Test Hebrew search term"""
        text = "זוהי משפט בעברית עם מילה חשובה בתוך הטקסט"
        result = highlight_search_term(text, "חשובה", 50)
        assert "חשובה" in result
    
    def test_term_not_found(self):
        """Test term not in text"""
        text = "This is some text"
        result = highlight_search_term(text, "missing", 50)
        assert "missing" not in result
    
    def test_empty_text(self):
        """Test empty text"""
        result = highlight_search_term("", "test", 50)
        assert result == ""


class TestFuzzyMatching:
    """Integration tests for fuzzy matching scenarios"""
    
    def test_similar_hebrew_vendors(self):
        """Test similarity between similar Hebrew vendor names"""
        vendor1 = "סופר מרקט"
        vendor2 = "סופר מרקט חדש"
        
        norm1 = normalize_hebrew_text(vendor1)
        norm2 = normalize_hebrew_text(vendor2)
        
        from difflib import SequenceMatcher
        similarity = SequenceMatcher(None, norm1, norm2).ratio() * 100
        
        # Should be reasonably similar
        assert similarity > 70
    
    def test_different_hebrew_vendors(self):
        """Test similarity between different Hebrew vendors"""
        vendor1 = "סופר מרקט"
        vendor2 = "מסעדה"
        
        norm1 = normalize_hebrew_text(vendor1)
        norm2 = normalize_hebrew_text(vendor2)
        
        from difflib import SequenceMatcher
        similarity = SequenceMatcher(None, norm1, norm2).ratio() * 100
        
        # Should be low similarity
        assert similarity < 30
    
    def test_typo_tolerance(self):
        """Test tolerance for typos"""
        vendor1 = "סופר פארם"
        vendor2 = "סופר פרם"  # Missing 'א'
        
        norm1 = normalize_hebrew_text(vendor1)
        norm2 = normalize_hebrew_text(vendor2)
        
        from difflib import SequenceMatcher
        similarity = SequenceMatcher(None, norm1, norm2).ratio() * 100
        
        # Should be very similar despite typo
        assert similarity > 85
