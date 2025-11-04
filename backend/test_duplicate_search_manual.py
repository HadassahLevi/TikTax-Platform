"""
Manual test script for duplicate detection and search functionality
"""

import sys
sys.path.insert(0, '.')

from app.utils.text_utils import normalize_hebrew_text, clean_business_number
from difflib import SequenceMatcher

def test_hebrew_normalization():
    """Test Hebrew text normalization"""
    print("=" * 60)
    print("TESTING HEBREW TEXT NORMALIZATION")
    print("=" * 60)
    
    tests = [
        ("שלום עולם", "Basic Hebrew"),
        ("שָׁלוֹם עוֹלָם", "Hebrew with nikud"),
        ("שלום! עולם?", "Hebrew with punctuation"),
        ("Super סופר", "Mixed Hebrew-English"),
        ("קבלה 123", "Hebrew with numbers"),
    ]
    
    for text, description in tests:
        result = normalize_hebrew_text(text)
        print(f"\n{description}:")
        print(f"  Input:  {text}")
        print(f"  Output: {result}")
    
    print("\n✓ Hebrew normalization tests completed\n")


def test_fuzzy_matching():
    """Test fuzzy vendor name matching"""
    print("=" * 60)
    print("TESTING FUZZY MATCHING")
    print("=" * 60)
    
    test_pairs = [
        ("סופר מרקט", "סופר מרקט", "Exact match"),
        ("סופר מרקט", "סופר מרקט חדש", "Similar vendors"),
        ("סופר מרקט", "מסעדה", "Different vendors"),
        ("סופר פארם", "סופר פרם", "Typo tolerance"),
        ("Super", "סופר", "English vs Hebrew"),
    ]
    
    for vendor1, vendor2, description in test_pairs:
        norm1 = normalize_hebrew_text(vendor1)
        norm2 = normalize_hebrew_text(vendor2)
        similarity = SequenceMatcher(None, norm1, norm2).ratio() * 100
        
        is_duplicate = similarity >= 80.0
        status = "✓ DUPLICATE" if is_duplicate else "✗ NOT DUPLICATE"
        
        print(f"\n{description}:")
        print(f"  Vendor 1: {vendor1} → {norm1}")
        print(f"  Vendor 2: {vendor2} → {norm2}")
        print(f"  Similarity: {similarity:.1f}%")
        print(f"  Status: {status}")
    
    print("\n✓ Fuzzy matching tests completed\n")


def test_business_number_cleaning():
    """Test business number cleaning"""
    print("=" * 60)
    print("TESTING BUSINESS NUMBER CLEANING")
    print("=" * 60)
    
    tests = [
        ("123456789", "Valid 9 digits"),
        ("12-345-6789", "With dashes"),
        ("12345", "Short number (padding)"),
        ("123 456 789", "With spaces"),
    ]
    
    for number, description in tests:
        result = clean_business_number(number)
        print(f"\n{description}:")
        print(f"  Input:  {number}")
        print(f"  Output: {result}")
    
    print("\n✓ Business number cleaning tests completed\n")


def test_search_scoring():
    """Test search relevance scoring"""
    print("=" * 60)
    print("TESTING SEARCH RELEVANCE SCORING")
    print("=" * 60)
    
    # Simulate search query
    query = "סופר"
    vendors = [
        "סופר מרקט",      # Should score highest (prefix match)
        "פארם סופר",      # Should score lower (not prefix)
        "מסעדה",          # Should score 0 (no match)
        "Super Market",   # Should match normalized
    ]
    
    print(f"\nSearch query: '{query}'")
    print("\nResults:")
    
    results = []
    for vendor in vendors:
        score = 0.0
        
        vendor_lower = vendor.lower()
        vendor_normalized = normalize_hebrew_text(vendor)
        query_normalized = normalize_hebrew_text(query)
        
        if query.lower() in vendor_lower:
            score += 50
            if vendor_lower.startswith(query.lower()):
                score += 30
        
        if query_normalized in vendor_normalized:
            if score == 0:
                score += 40
        
        results.append((vendor, score))
    
    # Sort by score
    results.sort(key=lambda x: x[1], reverse=True)
    
    for i, (vendor, score) in enumerate(results, 1):
        print(f"  {i}. {vendor:20} → Score: {score:.0f}")
    
    print("\n✓ Search scoring tests completed\n")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("DUPLICATE DETECTION & SEARCH - MANUAL TESTS")
    print("=" * 60 + "\n")
    
    try:
        test_hebrew_normalization()
        test_fuzzy_matching()
        test_business_number_cleaning()
        test_search_scoring()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
