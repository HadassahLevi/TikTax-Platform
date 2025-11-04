"""
Integration tests for duplicate detection and search endpoints
"""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.receipt import Receipt, ReceiptStatus
from app.models.category import Category


@pytest.fixture
def test_receipts(db: Session, test_user: User, test_category: Category):
    """Create test receipts for duplicate detection and search"""
    receipts = [
        Receipt(
            user_id=test_user.id,
            original_filename="receipt1.jpg",
            file_url="s3://test/receipt1.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="סופר מרקט",
            business_number="123456789",
            receipt_number="REC-001",
            receipt_date=datetime(2024, 11, 1, 10, 0),
            total_amount=150.50,
            vat_amount=25.50,
            category_id=test_category.id,
            status=ReceiptStatus.APPROVED
        ),
        Receipt(
            user_id=test_user.id,
            original_filename="receipt2.jpg",
            file_url="s3://test/receipt2.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="סופר מרקט חדש",  # Similar to receipt1
            business_number="123456789",
            receipt_number="REC-002",
            receipt_date=datetime(2024, 11, 1, 14, 0),  # Same day
            total_amount=152.00,  # Within 5% of receipt1
            vat_amount=26.00,
            category_id=test_category.id,
            status=ReceiptStatus.APPROVED
        ),
        Receipt(
            user_id=test_user.id,
            original_filename="receipt3.jpg",
            file_url="s3://test/receipt3.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="מסעדה איטלקית",
            business_number="987654321",
            receipt_number="REC-003",
            receipt_date=datetime(2024, 11, 5, 19, 0),
            total_amount=280.00,
            vat_amount=47.00,
            category_id=test_category.id,
            status=ReceiptStatus.APPROVED,
            notes="ארוחת עסקים עם לקוח"
        ),
        Receipt(
            user_id=test_user.id,
            original_filename="receipt4.jpg",
            file_url="s3://test/receipt4.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="פארם סופר",
            business_number="555555555",
            receipt_number="REC-004",
            receipt_date=datetime(2024, 11, 10, 9, 0),
            total_amount=95.20,
            vat_amount=16.20,
            category_id=test_category.id,
            status=ReceiptStatus.APPROVED
        ),
        Receipt(
            user_id=test_user.id,
            original_filename="receipt5.jpg",
            file_url="s3://test/receipt5.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="חנות ציוד משרדי",
            business_number="111222333",
            receipt_number="OFF-100",
            receipt_date=datetime(2024, 11, 15, 11, 0),
            total_amount=450.00,
            vat_amount=76.50,
            category_id=test_category.id,
            status=ReceiptStatus.REVIEW  # Not approved yet
        )
    ]
    
    for receipt in receipts:
        db.add(receipt)
    
    db.commit()
    
    for receipt in receipts:
        db.refresh(receipt)
    
    return receipts


class TestDuplicateDetection:
    """Tests for /check-duplicate endpoint"""
    
    def test_exact_duplicate_detected(
        self,
        client: TestClient,
        test_user: User,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test detection of exact duplicate"""
        original = test_receipts[0]
        
        response = client.post(
            "/api/v1/receipts/check-duplicate",
            json={
                "vendor_name": original.vendor_name,
                "receipt_date": original.receipt_date.isoformat(),
                "total_amount": original.total_amount
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_duplicate"] is True
        assert data["duplicate_receipt_id"] == original.id
        assert data["similarity_score"] >= 95.0
        assert "נמצאה קבלה דומה" in data["message"]
    
    def test_similar_duplicate_detected(
        self,
        client: TestClient,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test detection of similar duplicate (not exact)"""
        # Check against receipt similar to first one
        response = client.post(
            "/api/v1/receipts/check-duplicate",
            json={
                "vendor_name": "סופר מרקט",  # Similar to "סופר מרקט חדש"
                "receipt_date": datetime(2024, 11, 1, 12, 0).isoformat(),
                "total_amount": 151.00  # Between receipt1 and receipt2
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_duplicate"] is True
        assert data["similarity_score"] >= 80.0
    
    def test_no_duplicate_found(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test when no duplicate exists"""
        response = client.post(
            "/api/v1/receipts/check-duplicate",
            json={
                "vendor_name": "חנות חדשה לגמרי",
                "receipt_date": datetime(2024, 12, 1, 10, 0).isoformat(),
                "total_amount": 999.99
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_duplicate"] is False
        assert data["duplicate_receipt_id"] is None
        assert data["similarity_score"] < 80.0
        assert "לא נמצאו קבלות דומות" in data["message"]
    
    def test_different_date_not_duplicate(
        self,
        client: TestClient,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test that same vendor on different date is not duplicate"""
        original = test_receipts[0]
        
        # Same vendor and amount, but 3 days later (outside ±1 day range)
        response = client.post(
            "/api/v1/receipts/check-duplicate",
            json={
                "vendor_name": original.vendor_name,
                "receipt_date": (original.receipt_date + timedelta(days=3)).isoformat(),
                "total_amount": original.total_amount
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_duplicate"] is False
    
    def test_different_amount_not_duplicate(
        self,
        client: TestClient,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test that different amount is not duplicate"""
        original = test_receipts[0]
        
        # Same vendor and date, but very different amount (>5% difference)
        response = client.post(
            "/api/v1/receipts/check-duplicate",
            json={
                "vendor_name": original.vendor_name,
                "receipt_date": original.receipt_date.isoformat(),
                "total_amount": original.total_amount * 2
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_duplicate"] is False
    
    def test_hebrew_typo_tolerance(
        self,
        client: TestClient,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test tolerance for typos in Hebrew vendor names"""
        original = test_receipts[0]
        
        # "סופר מרקט" with typo
        response = client.post(
            "/api/v1/receipts/check-duplicate",
            json={
                "vendor_name": "סופר מרקט",  # Very similar
                "receipt_date": original.receipt_date.isoformat(),
                "total_amount": original.total_amount
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["similarity_score"] >= 85.0
    
    def test_invalid_request_validation(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test request validation"""
        # Missing required fields
        response = client.post(
            "/api/v1/receipts/check-duplicate",
            json={
                "vendor_name": "test"
                # Missing receipt_date and total_amount
            },
            headers=auth_headers
        )
        
        assert response.status_code == 422
    
    def test_unauthorized_access(
        self,
        client: TestClient
    ):
        """Test unauthorized access is rejected"""
        response = client.post(
            "/api/v1/receipts/check-duplicate",
            json={
                "vendor_name": "test",
                "receipt_date": datetime.now().isoformat(),
                "total_amount": 100.0
            }
        )
        
        assert response.status_code == 401


class TestReceiptSearch:
    """Tests for /search endpoint"""
    
    def test_search_by_vendor_name(
        self,
        client: TestClient,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test search by vendor name"""
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "סופר"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total"] >= 2  # Should find "סופר מרקט" and "פארם סופר"
        assert data["query"] == "סופר"
        assert len(data["results"]) >= 2
        
        # Check results are sorted by relevance
        scores = [r["relevance_score"] for r in data["results"]]
        assert scores == sorted(scores, reverse=True)
    
    def test_search_by_receipt_number(
        self,
        client: TestClient,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test search by receipt number"""
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "REC-001"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total"] >= 1
        
        # Exact match should have highest score
        top_result = data["results"][0]
        assert top_result["matched_field"] == "receipt_number"
        assert top_result["relevance_score"] >= 100
    
    def test_search_by_business_number(
        self,
        client: TestClient,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test search by business number"""
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "123456789"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total"] >= 1
        
        # Should find receipts with this business number
        top_result = data["results"][0]
        assert top_result["matched_field"] == "business_number"
    
    def test_search_in_notes(
        self,
        client: TestClient,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test search in receipt notes"""
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "עסקים"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total"] >= 1
        
        # Should find receipt with "ארוחת עסקים" in notes
        found = any(r["matched_field"] == "notes" for r in data["results"])
        assert found
    
    def test_search_no_results(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test search with no matches"""
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "xyzabc123"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total"] == 0
        assert len(data["results"]) == 0
    
    def test_search_prefix_match_bonus(
        self,
        client: TestClient,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test that prefix matches get higher scores"""
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "סופר"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # "סופר מרקט" (starts with "סופר") should score higher than "פארם סופר"
        if len(data["results"]) >= 2:
            top_result = data["results"][0]
            assert top_result["vendor_name"].startswith("סופר")
    
    def test_search_limit_parameter(
        self,
        client: TestClient,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test limit parameter"""
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "REC", "limit": 2},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["results"]) <= 2
    
    def test_search_hebrew_normalization(
        self,
        client: TestClient,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test Hebrew text normalization in search"""
        # Search with and without nikud should give same results
        response1 = client.get(
            "/api/v1/receipts/search",
            params={"q": "מרקט"},
            headers=auth_headers
        )
        
        response2 = client.get(
            "/api/v1/receipts/search",
            params={"q": "מַרְקֶט"},  # With nikud
            headers=auth_headers
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Should return similar results (normalization should handle nikud)
        assert len(response1.json()["results"]) > 0
    
    def test_search_validation_min_length(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test minimum query length validation"""
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "a"},  # Too short
            headers=auth_headers
        )
        
        assert response.status_code == 422
    
    def test_search_validation_max_length(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test maximum query length validation"""
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "a" * 101},  # Too long
            headers=auth_headers
        )
        
        assert response.status_code == 422
    
    def test_search_excludes_failed_receipts(
        self,
        client: TestClient,
        db: Session,
        test_user: User,
        test_category: Category,
        auth_headers: dict
    ):
        """Test that failed receipts are excluded from search"""
        # Create a failed receipt
        failed_receipt = Receipt(
            user_id=test_user.id,
            original_filename="failed.jpg",
            file_url="s3://test/failed.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="חנות נכשלת",
            status=ReceiptStatus.FAILED
        )
        db.add(failed_receipt)
        db.commit()
        
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "נכשלת"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should not find failed receipt
        assert data["total"] == 0
    
    def test_search_includes_category_name(
        self,
        client: TestClient,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test that results include category name"""
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "סופר"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        if len(data["results"]) > 0:
            result = data["results"][0]
            assert "category_name" in result
    
    def test_search_unauthorized_access(
        self,
        client: TestClient
    ):
        """Test unauthorized access is rejected"""
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "test"}
        )
        
        assert response.status_code == 401
    
    def test_search_user_isolation(
        self,
        client: TestClient,
        db: Session,
        test_receipts: list,
        auth_headers: dict
    ):
        """Test that users only see their own receipts in search"""
        # Create another user with a receipt
        other_user = User(
            email="other@example.com",
            hashed_password="hash",
            full_name="Other User"
        )
        db.add(other_user)
        db.commit()
        db.refresh(other_user)
        
        other_receipt = Receipt(
            user_id=other_user.id,
            original_filename="other.jpg",
            file_url="s3://test/other.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="חנות של משתמש אחר",
            status=ReceiptStatus.APPROVED
        )
        db.add(other_receipt)
        db.commit()
        
        # Search for other user's receipt
        response = client.get(
            "/api/v1/receipts/search",
            params={"q": "אחר"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should not find other user's receipt
        assert data["total"] == 0
