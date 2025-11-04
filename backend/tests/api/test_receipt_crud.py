"""
Unit Tests for Receipt CRUD Endpoints
Tests all receipt management operations
"""

import pytest
from datetime import datetime, timedelta
from fastapi import status
from sqlalchemy.orm import Session

from app.models.receipt import Receipt, ReceiptStatus
from app.models.user import User
from app.models.category import Category
from app.schemas.receipt import ReceiptUpdate, ReceiptApprove


class TestListReceipts:
    """Test GET /api/v1/receipts endpoint"""
    
    def test_list_receipts_success(self, client, test_user, auth_headers, db):
        """Test listing receipts with pagination"""
        # Create test receipts
        for i in range(5):
            receipt = Receipt(
                user_id=test_user.id,
                original_filename=f"receipt_{i}.jpg",
                file_url=f"https://s3.amazonaws.com/receipts/receipt_{i}.jpg",
                file_size=1024 * (i + 1),
                mime_type="image/jpeg",
                vendor_name=f"Vendor {i}",
                total_amount=100.0 + i * 10,
                receipt_date=datetime.utcnow() - timedelta(days=i),
                status=ReceiptStatus.APPROVED,
                is_digitally_signed=False,
                is_duplicate=False
            )
            db.add(receipt)
        db.commit()
        
        # Test request
        response = client.get("/api/v1/receipts", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 5
        assert len(data["receipts"]) == 5
        assert data["page"] == 1
        assert data["page_size"] == 20
        assert data["pages"] == 1
    
    def test_list_receipts_pagination(self, client, test_user, auth_headers, db):
        """Test pagination works correctly"""
        # Create 25 receipts
        for i in range(25):
            receipt = Receipt(
                user_id=test_user.id,
                original_filename=f"receipt_{i}.jpg",
                file_url=f"https://s3.amazonaws.com/receipts/receipt_{i}.jpg",
                file_size=1024,
                mime_type="image/jpeg",
                status=ReceiptStatus.APPROVED,
                is_digitally_signed=False,
                is_duplicate=False
            )
            db.add(receipt)
        db.commit()
        
        # Request page 2 with page_size 10
        response = client.get(
            "/api/v1/receipts",
            params={"page": 2, "page_size": 10},
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 25
        assert len(data["receipts"]) == 10
        assert data["page"] == 2
        assert data["pages"] == 3
    
    def test_list_receipts_filter_by_date(self, client, test_user, auth_headers, db):
        """Test filtering by date range"""
        # Create receipts with different dates
        receipt1 = Receipt(
            user_id=test_user.id,
            original_filename="receipt1.jpg",
            file_url="https://s3.amazonaws.com/receipts/receipt1.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            receipt_date=datetime(2024, 1, 15),
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        receipt2 = Receipt(
            user_id=test_user.id,
            original_filename="receipt2.jpg",
            file_url="https://s3.amazonaws.com/receipts/receipt2.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            receipt_date=datetime(2024, 2, 15),
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add_all([receipt1, receipt2])
        db.commit()
        
        # Filter for January only
        response = client.get(
            "/api/v1/receipts",
            params={
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2024-01-31T23:59:59"
            },
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert data["receipts"][0]["receipt_date"].startswith("2024-01")
    
    def test_list_receipts_filter_by_category(self, client, test_user, auth_headers, db):
        """Test filtering by category"""
        # Create category
        category = Category(name_hebrew="מזון", name_english="Food", icon="🍔")
        db.add(category)
        db.commit()
        
        # Create receipts
        receipt1 = Receipt(
            user_id=test_user.id,
            original_filename="receipt1.jpg",
            file_url="https://s3.amazonaws.com/receipts/receipt1.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            category_id=category.id,
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        receipt2 = Receipt(
            user_id=test_user.id,
            original_filename="receipt2.jpg",
            file_url="https://s3.amazonaws.com/receipts/receipt2.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            category_id=None,
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add_all([receipt1, receipt2])
        db.commit()
        
        # Filter by category
        response = client.get(
            "/api/v1/receipts",
            params={"category_ids": str(category.id)},
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert data["receipts"][0]["category_name"] == "מזון"
    
    def test_list_receipts_filter_by_amount(self, client, test_user, auth_headers, db):
        """Test filtering by amount range"""
        # Create receipts with different amounts
        for i, amount in enumerate([50.0, 100.0, 150.0, 200.0]):
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
        
        # Filter for amounts between 75 and 175
        response = client.get(
            "/api/v1/receipts",
            params={"amount_min": 75.0, "amount_max": 175.0},
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 2  # 100 and 150
    
    def test_list_receipts_search(self, client, test_user, auth_headers, db):
        """Test search functionality"""
        receipt1 = Receipt(
            user_id=test_user.id,
            original_filename="receipt1.jpg",
            file_url="https://s3.amazonaws.com/receipts/receipt1.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="Super-Pharm",
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        receipt2 = Receipt(
            user_id=test_user.id,
            original_filename="receipt2.jpg",
            file_url="https://s3.amazonaws.com/receipts/receipt2.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="McDonald's",
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add_all([receipt1, receipt2])
        db.commit()
        
        # Search for "pharm"
        response = client.get(
            "/api/v1/receipts",
            params={"search_query": "pharm"},
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert "Pharm" in data["receipts"][0]["vendor_name"]
    
    def test_list_receipts_sorting(self, client, test_user, auth_headers, db):
        """Test sorting functionality"""
        # Create receipts with different amounts
        for i, amount in enumerate([150.0, 50.0, 200.0, 100.0]):
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
        
        # Sort by amount ascending
        response = client.get(
            "/api/v1/receipts",
            params={"sort_by": "total_amount", "sort_order": "asc"},
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        amounts = [r["total_amount"] for r in data["receipts"]]
        assert amounts == [50.0, 100.0, 150.0, 200.0]
    
    def test_list_receipts_only_own(self, client, test_user, auth_headers, db):
        """Test user can only see their own receipts"""
        # Create another user and their receipt
        other_user = User(
            email="other@test.com",
            hashed_password="hashed",
            full_name="Other User",
            phone_number="0501234567",
            is_active=True,
            is_verified=True
        )
        db.add(other_user)
        db.commit()
        
        other_receipt = Receipt(
            user_id=other_user.id,
            original_filename="other.jpg",
            file_url="https://s3.amazonaws.com/receipts/other.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(other_receipt)
        db.commit()
        
        # Request receipts
        response = client.get("/api/v1/receipts", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 0  # Should not see other user's receipt


class TestGetReceipt:
    """Test GET /api/v1/receipts/{receipt_id} endpoint"""
    
    def test_get_receipt_success(self, client, test_user, auth_headers, db):
        """Test getting single receipt"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/receipts/test.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="Test Vendor",
            total_amount=100.0,
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(receipt)
        db.commit()
        
        response = client.get(f"/api/v1/receipts/{receipt.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == receipt.id
        assert data["vendor_name"] == "Test Vendor"
        assert data["total_amount"] == 100.0
    
    def test_get_receipt_not_found(self, client, test_user, auth_headers, db):
        """Test 404 for non-existent receipt"""
        response = client.get("/api/v1/receipts/99999", headers=auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "לא נמצאה" in response.json()["detail"]
    
    def test_get_receipt_wrong_user(self, client, test_user, auth_headers, db):
        """Test user cannot access another user's receipt"""
        # Create another user and their receipt
        other_user = User(
            email="other@test.com",
            hashed_password="hashed",
            full_name="Other User",
            phone_number="0501234567",
            is_active=True,
            is_verified=True
        )
        db.add(other_user)
        db.commit()
        
        other_receipt = Receipt(
            user_id=other_user.id,
            original_filename="other.jpg",
            file_url="https://s3.amazonaws.com/receipts/other.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(other_receipt)
        db.commit()
        
        response = client.get(f"/api/v1/receipts/{other_receipt.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateReceipt:
    """Test PUT /api/v1/receipts/{receipt_id} endpoint"""
    
    def test_update_receipt_success(self, client, test_user, auth_headers, db):
        """Test updating receipt in REVIEW status"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/receipts/test.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="Original Vendor",
            total_amount=100.0,
            status=ReceiptStatus.REVIEW,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(receipt)
        db.commit()
        
        update_data = {
            "vendor_name": "Updated Vendor",
            "total_amount": 150.0,
            "notes": "Updated notes"
        }
        
        response = client.put(
            f"/api/v1/receipts/{receipt.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["vendor_name"] == "Updated Vendor"
        assert data["total_amount"] == 150.0
        assert data["notes"] == "Updated notes"
    
    def test_update_receipt_creates_edit_history(self, client, test_user, auth_headers, db):
        """Test that updates create edit history records"""
        from app.models.receipt_edit import ReceiptEdit
        
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/receipts/test.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            vendor_name="Original",
            status=ReceiptStatus.REVIEW,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(receipt)
        db.commit()
        
        update_data = {"vendor_name": "Updated"}
        
        response = client.put(
            f"/api/v1/receipts/{receipt.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check edit history
        edits = db.query(ReceiptEdit).filter(ReceiptEdit.receipt_id == receipt.id).all()
        assert len(edits) == 1
        assert edits[0].field_name == "vendor_name"
        assert edits[0].old_value == "Original"
        assert edits[0].new_value == "Updated"
    
    def test_update_receipt_cannot_edit_approved(self, client, test_user, auth_headers, db):
        """Test cannot update approved receipts"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/receipts/test.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(receipt)
        db.commit()
        
        update_data = {"vendor_name": "Updated"}
        
        response = client.put(
            f"/api/v1/receipts/{receipt.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "לא ניתן לערוך" in response.json()["detail"]
    
    def test_update_receipt_validates_business_number(self, client, test_user, auth_headers, db):
        """Test business number validation"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/receipts/test.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            status=ReceiptStatus.REVIEW,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(receipt)
        db.commit()
        
        # Invalid business number (not 9 digits)
        update_data = {"business_number": "12345"}
        
        response = client.put(
            f"/api/v1/receipts/{receipt.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestApproveReceipt:
    """Test POST /api/v1/receipts/{receipt_id}/approve endpoint"""
    
    def test_approve_receipt_success(self, client, test_user, auth_headers, db):
        """Test approving receipt"""
        category = Category(name_hebrew="מזון", name_english="Food", icon="🍔")
        db.add(category)
        db.commit()
        
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/receipts/test.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            status=ReceiptStatus.REVIEW,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(receipt)
        db.commit()
        
        approve_data = {
            "vendor_name": "Test Vendor",
            "receipt_date": datetime.utcnow().isoformat(),
            "total_amount": 100.0,
            "category_id": category.id
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
    
    def test_approve_receipt_cannot_approve_twice(self, client, test_user, auth_headers, db):
        """Test cannot approve already approved receipt"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/receipts/test.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(receipt)
        db.commit()
        
        approve_data = {
            "vendor_name": "Test",
            "receipt_date": datetime.utcnow().isoformat(),
            "total_amount": 100.0,
            "category_id": 1
        }
        
        response = client.post(
            f"/api/v1/receipts/{receipt.id}/approve",
            json=approve_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteReceipt:
    """Test DELETE /api/v1/receipts/{receipt_id} endpoint"""
    
    def test_delete_receipt_success(self, client, test_user, auth_headers, db):
        """Test deleting receipt"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/receipts/test.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(receipt)
        db.commit()
        
        receipt_id = receipt.id
        
        response = client.delete(f"/api/v1/receipts/{receipt_id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify deleted
        deleted_receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
        assert deleted_receipt is None
    
    def test_delete_receipt_not_found(self, client, test_user, auth_headers, db):
        """Test 404 when deleting non-existent receipt"""
        response = client.delete("/api/v1/receipts/99999", headers=auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestRetryProcessing:
    """Test POST /api/v1/receipts/{receipt_id}/retry endpoint"""
    
    def test_retry_processing_success(self, client, test_user, auth_headers, db):
        """Test retrying failed receipt"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/receipts/test.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            status=ReceiptStatus.FAILED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(receipt)
        db.commit()
        
        response = client.post(
            f"/api/v1/receipts/{receipt.id}/retry",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert "מעבד מחדש" in response.json()["message"]
        
        # Verify status changed
        db.refresh(receipt)
        assert receipt.status == ReceiptStatus.PROCESSING
    
    def test_retry_processing_only_failed(self, client, test_user, auth_headers, db):
        """Test can only retry failed receipts"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/receipts/test.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            status=ReceiptStatus.APPROVED,
            is_digitally_signed=False,
            is_duplicate=False
        )
        db.add(receipt)
        db.commit()
        
        response = client.post(
            f"/api/v1/receipts/{receipt.id}/retry",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "שנכשלו" in response.json()["detail"]
