"""
Integration Tests for Receipt CRUD Endpoints
Tests complete workflows with database interactions
"""

import pytest
from datetime import datetime, timedelta
from fastapi import status
from sqlalchemy.orm import Session

from app.models.receipt import Receipt, ReceiptStatus
from app.models.user import User
from app.models.category import Category
from app.models.receipt_edit import ReceiptEdit


class TestReceiptCRUDWorkflow:
    """Test complete CRUD workflow"""
    
    def test_complete_receipt_lifecycle(self, client, test_user, auth_headers, db):
        """Test complete receipt workflow from creation to deletion"""
        # 1. Create category
        category = Category(
            name_hebrew="תחבורה",
            name_english="Transportation",
            icon="🚗"
        )
        db.add(category)
        db.commit()
        
        # 2. Create receipt (simulating upload)
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="receipt.jpg",
            file_url="https://s3.amazonaws.com/receipts/receipt.jpg",
            file_size=2048,
            mime_type="image/jpeg",
            vendor_name="דלק",
            total_amount=200.0,
            receipt_date=datetime.utcnow(),
            status=ReceiptStatus.REVIEW,
            confidence_score=0.85,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(receipt)
        db.commit()
        
        # 3. Get receipt details
        response = client.get(f"/api/v1/receipts/{receipt.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["vendor_name"] == "דלק"
        assert data["status"] == "review"
        
        # 4. Update receipt
        update_data = {
            "vendor_name": "דלק - תחנת דלק",
            "total_amount": 210.0,
            "category_id": category.id,
            "notes": "תדלוק מלא"
        }
        response = client.put(
            f"/api/v1/receipts/{receipt.id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify edit history created
        edits = db.query(ReceiptEdit).filter(ReceiptEdit.receipt_id == receipt.id).all()
        assert len(edits) > 0
        
        # 5. Approve receipt
        approve_data = {
            "vendor_name": "דלק - תחנת דלק",
            "receipt_date": datetime.utcnow().isoformat(),
            "total_amount": 210.0,
            "category_id": category.id,
            "notes": "תדלוק מלא"
        }
        response = client.post(
            f"/api/v1/receipts/{receipt.id}/approve",
            json=approve_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "approved"
        assert data["approved_at"] is not None
        
        # 6. List receipts (should include approved receipt)
        response = client.get("/api/v1/receipts", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert data["receipts"][0]["category_name"] == "תחבורה"
        
        # 7. Delete receipt
        response = client.delete(f"/api/v1/receipts/{receipt.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify deletion
        deleted = db.query(Receipt).filter(Receipt.id == receipt.id).first()
        assert deleted is None


class TestReceiptFiltering:
    """Test advanced filtering scenarios"""
    
    def test_complex_filtering(self, client, test_user, auth_headers, db):
        """Test combining multiple filters"""
        # Create categories
        food = Category(name_hebrew="מזון", name_english="Food", icon="🍔")
        transport = Category(name_hebrew="תחבורה", name_english="Transport", icon="🚗")
        db.add_all([food, transport])
        db.commit()
        
        # Create receipts
        receipts_data = [
            {
                "vendor_name": "מסעדה",
                "amount": 150.0,
                "date": datetime(2024, 1, 15),
                "category": food.id,
                "status": ReceiptStatus.APPROVED
            },
            {
                "vendor_name": "דלק",
                "amount": 300.0,
                "date": datetime(2024, 1, 20),
                "category": transport.id,
                "status": ReceiptStatus.APPROVED
            },
            {
                "vendor_name": "קפה",
                "amount": 50.0,
                "date": datetime(2024, 2, 1),
                "category": food.id,
                "status": ReceiptStatus.REVIEW
            },
            {
                "vendor_name": "מונית",
                "amount": 80.0,
                "date": datetime(2024, 2, 5),
                "category": transport.id,
                "status": ReceiptStatus.APPROVED
            }
        ]
        
        for data in receipts_data:
            receipt = Receipt(
                user_id=test_user.id,
                original_filename=f"{data['vendor_name']}.jpg",
                file_url=f"https://s3.amazonaws.com/receipts/{data['vendor_name']}.jpg",
                file_size=1024,
                mime_type="image/jpeg",
                vendor_name=data["vendor_name"],
                total_amount=data["amount"],
                receipt_date=data["date"],
                category_id=data["category"],
                status=data["status"],
                is_digitally_signed=False,
                is_duplicate=False
            )
            db.add(receipt)
        db.commit()
        
        # Test 1: Filter by date range + category + status
        response = client.get(
            "/api/v1/receipts",
            params={
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2024-01-31T23:59:59",
                "category_ids": f"{food.id}",
                "status": "approved"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1  # Only מסעדה matches
        assert data["receipts"][0]["vendor_name"] == "מסעדה"
        
        # Test 2: Filter by amount range + multiple categories
        response = client.get(
            "/api/v1/receipts",
            params={
                "amount_min": 100.0,
                "amount_max": 350.0,
                "category_ids": f"{food.id},{transport.id}"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 2  # מסעדה (150) and דלק (300)
        
        # Test 3: Search + date range
        response = client.get(
            "/api/v1/receipts",
            params={
                "search_query": "קפה",
                "date_from": "2024-02-01T00:00:00"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert data["receipts"][0]["vendor_name"] == "קפה"


class TestReceiptPagination:
    """Test pagination edge cases"""
    
    def test_large_dataset_pagination(self, client, test_user, auth_headers, db):
        """Test pagination with large dataset"""
        # Create 100 receipts
        for i in range(100):
            receipt = Receipt(
                user_id=test_user.id,
                original_filename=f"receipt_{i}.jpg",
                file_url=f"https://s3.amazonaws.com/receipts/receipt_{i}.jpg",
                file_size=1024,
                mime_type="image/jpeg",
                vendor_name=f"Vendor {i}",
                total_amount=float(i + 1),
                receipt_date=datetime.utcnow() - timedelta(days=i),
                status=ReceiptStatus.APPROVED,
                is_digitally_signed=False,
                is_duplicate=False
            )
            db.add(receipt)
        db.commit()
        
        # Test first page
        response = client.get(
            "/api/v1/receipts",
            params={"page": 1, "page_size": 20},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 100
        assert len(data["receipts"]) == 20
        assert data["pages"] == 5
        
        # Test last page
        response = client.get(
            "/api/v1/receipts",
            params={"page": 5, "page_size": 20},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["receipts"]) == 20
        
        # Test beyond last page
        response = client.get(
            "/api/v1/receipts",
            params={"page": 6, "page_size": 20},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["receipts"]) == 0
    
    def test_pagination_with_filters(self, client, test_user, auth_headers, db):
        """Test pagination works correctly with filters"""
        # Create 50 receipts, half with high amounts
        for i in range(50):
            amount = 200.0 if i < 25 else 50.0
            receipt = Receipt(
                user_id=test_user.id,
                original_filename=f"receipt_{i}.jpg",
                file_url=f"https://s3.amazonaws.com/receipts/receipt_{i}.jpg",
                file_size=1024,
                mime_type="image/jpeg",
                total_amount=amount,
                status=ReceiptStatus.APPROVED,
                is_digitally_signed=False,
                is_duplicate=False
            )
            db.add(receipt)
        db.commit()
        
        # Filter for high amounts and paginate
        response = client.get(
            "/api/v1/receipts",
            params={"amount_min": 150.0, "page": 1, "page_size": 10},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 25
        assert len(data["receipts"]) == 10
        assert data["pages"] == 3


class TestReceiptEditHistory:
    """Test edit history tracking"""
    
    def test_multiple_edits_create_history(self, client, test_user, auth_headers, db):
        """Test multiple edits create separate history records"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/receipts/test.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="Original",
            total_amount=100.0,
            status=ReceiptStatus.REVIEW,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(receipt)
        db.commit()
        
        # First edit
        client.put(
            f"/api/v1/receipts/{receipt.id}",
            json={"vendor_name": "Edit 1"},
            headers=auth_headers
        )
        
        # Second edit
        client.put(
            f"/api/v1/receipts/{receipt.id}",
            json={"total_amount": 200.0},
            headers=auth_headers
        )
        
        # Third edit
        client.put(
            f"/api/v1/receipts/{receipt.id}",
            json={"notes": "Added notes"},
            headers=auth_headers
        )
        
        # Check edit history
        edits = db.query(ReceiptEdit).filter(
            ReceiptEdit.receipt_id == receipt.id
        ).order_by(ReceiptEdit.edited_at).all()
        
        assert len(edits) == 3
        assert edits[0].field_name == "vendor_name"
        assert edits[0].new_value == "Edit 1"
        assert edits[1].field_name == "total_amount"
        assert edits[1].new_value == "200.0"
        assert edits[2].field_name == "notes"
        assert edits[2].new_value == "Added notes"


class TestReceiptSorting:
    """Test sorting functionality"""
    
    def test_sort_by_all_fields(self, client, test_user, auth_headers, db):
        """Test sorting by each sortable field"""
        # Create receipts with varied data
        receipts_data = [
            {"vendor": "AAA", "amount": 300.0, "date": datetime(2024, 3, 1)},
            {"vendor": "ZZZ", "amount": 100.0, "date": datetime(2024, 1, 1)},
            {"vendor": "MMM", "amount": 200.0, "date": datetime(2024, 2, 1)},
        ]
        
        for data in receipts_data:
            receipt = Receipt(
                user_id=test_user.id,
                original_filename="test.jpg",
                file_url="https://s3.amazonaws.com/receipts/test.jpg",
                file_size=1024,
                mime_type="image/jpeg",
                vendor_name=data["vendor"],
                total_amount=data["amount"],
                receipt_date=data["date"],
                status=ReceiptStatus.APPROVED,
                is_digitally_signed=False,
                is_duplicate=False
            )
            db.add(receipt)
        db.commit()
        
        # Sort by vendor name ascending
        response = client.get(
            "/api/v1/receipts",
            params={"sort_by": "vendor_name", "sort_order": "asc"},
            headers=auth_headers
        )
        data = response.json()
        vendors = [r["vendor_name"] for r in data["receipts"]]
        assert vendors == ["AAA", "MMM", "ZZZ"]
        
        # Sort by amount descending
        response = client.get(
            "/api/v1/receipts",
            params={"sort_by": "total_amount", "sort_order": "desc"},
            headers=auth_headers
        )
        data = response.json()
        amounts = [r["total_amount"] for r in data["receipts"]]
        assert amounts == [300.0, 200.0, 100.0]
        
        # Sort by date ascending
        response = client.get(
            "/api/v1/receipts",
            params={"sort_by": "receipt_date", "sort_order": "asc"},
            headers=auth_headers
        )
        data = response.json()
        dates = [r["receipt_date"] for r in data["receipts"]]
        assert dates[0] < dates[1] < dates[2]


class TestReceiptSecurity:
    """Test security and permission checks"""
    
    def test_user_isolation(self, client, db):
        """Test users can only access their own receipts"""
        # Create two users
        user1 = User(
            email="user1@test.com",
            hashed_password="hashed1",
            full_name="User 1",
            phone_number="0501234567",
            is_active=True,
            is_verified=True
        )
        user2 = User(
            email="user2@test.com",
            hashed_password="hashed2",
            full_name="User 2",
            phone_number="0507654321",
            is_active=True,
            is_verified=True
        )
        db.add_all([user1, user2])
        db.commit()
        
        # Create receipts for each user
        receipt1 = Receipt(
            user_id=user1.id,
            original_filename="user1.jpg",
            file_url="https://s3.amazonaws.com/receipts/user1.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="User 1 Receipt",
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        receipt2 = Receipt(
            user_id=user2.id,
            original_filename="user2.jpg",
            file_url="https://s3.amazonaws.com/receipts/user2.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="User 2 Receipt",
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add_all([receipt1, receipt2])
        db.commit()
        
        # Mock auth headers for user1
        from app.core.security import create_access_token
        token = create_access_token({"sub": user1.email})
        headers1 = {"Authorization": f"Bearer {token}"}
        
        # User 1 lists receipts - should only see their own
        response = client.get("/api/v1/receipts", headers=headers1)
        data = response.json()
        assert data["total"] == 1
        assert data["receipts"][0]["vendor_name"] == "User 1 Receipt"
        
        # User 1 tries to access User 2's receipt - should fail
        response = client.get(f"/api/v1/receipts/{receipt2.id}", headers=headers1)
        assert response.status_code == status.HTTP_404_NOT_FOUND
