"""
Comprehensive tests for receipt endpoints
"""
import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from app.models.receipt import Receipt, ReceiptStatus
from app.models.category import Category
from app.models.receipt_edit import ReceiptEdit
from datetime import datetime, timedelta
import json


class TestReceiptUpload:
    """Tests for receipt upload functionality"""
    
    def test_upload_jpg_success(self, client: TestClient, auth_headers: dict, db):
        """Test successful JPG upload"""
        file_content = b"fake image content that is long enough to pass validation" * 200
        files = {"file": ("receipt.jpg", BytesIO(file_content), "image/jpeg")}
        
        response = client.post("/api/v1/receipts/upload", headers=auth_headers, files=files)
        
        assert response.status_code == 201
        data = response.json()
        assert "receipt_id" in data
        assert data["status"] == "processing"
    
    def test_upload_png_success(self, client: TestClient, auth_headers: dict, db):
        """Test successful PNG upload"""
        file_content = b"fake png content" * 200
        files = {"file": ("receipt.png", BytesIO(file_content), "image/png")}
        
        response = client.post("/api/v1/receipts/upload", headers=auth_headers, files=files)
        assert response.status_code == 201
    
    def test_upload_heic_success(self, client: TestClient, auth_headers: dict, db):
        """Test successful HEIC upload (iPhone format)"""
        file_content = b"fake heic content" * 200
        files = {"file": ("receipt.heic", BytesIO(file_content), "image/heic")}
        
        response = client.post("/api/v1/receipts/upload", headers=auth_headers, files=files)
        assert response.status_code == 201
    
    def test_upload_invalid_file_type(self, client: TestClient, auth_headers: dict):
        """Test upload with PDF (invalid type)"""
        files = {"file": ("receipt.pdf", BytesIO(b"pdf content"), "application/pdf")}
        
        response = client.post("/api/v1/receipts/upload", headers=auth_headers, files=files)
        
        assert response.status_code == 400
        assert "לא נתמך" in response.json()["detail"]
    
    def test_upload_file_too_large(self, client: TestClient, auth_headers: dict):
        """Test upload > 10MB"""
        large_file = b"x" * (11 * 1024 * 1024)
        files = {"file": ("receipt.jpg", BytesIO(large_file), "image/jpeg")}
        
        response = client.post("/api/v1/receipts/upload", headers=auth_headers, files=files)
        assert response.status_code == 413
    
    def test_upload_file_too_small(self, client: TestClient, auth_headers: dict):
        """Test upload < 10KB"""
        small_file = b"tiny"
        files = {"file": ("receipt.jpg", BytesIO(small_file), "image/jpeg")}
        
        response = client.post("/api/v1/receipts/upload", headers=auth_headers, files=files)
        assert response.status_code == 400
    
    def test_upload_unauthorized(self, client: TestClient):
        """Test upload without auth"""
        files = {"file": ("receipt.jpg", BytesIO(b"content"), "image/jpeg")}
        response = client.post("/api/v1/receipts/upload", files=files)
        assert response.status_code == 401


class TestReceiptStatus:
    """Tests for processing status endpoint"""
    
    def test_get_status_processing(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test status for processing receipt"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/test.jpg",
            status=ReceiptStatus.PROCESSING
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        
        response = client.get(f"/api/v1/receipts/{receipt.id}/status", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["receipt_id"] == receipt.id
        assert data["status"] == "processing"
        assert data["progress"] == 50
        assert "message" in data
    
    def test_get_status_review(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test status for review receipt"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/test.jpg",
            status=ReceiptStatus.REVIEW,
            ocr_data={"vendor": "Test"}
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        
        response = client.get(f"/api/v1/receipts/{receipt.id}/status", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "review"
        assert data["progress"] == 80
    
    def test_get_status_not_found(self, client: TestClient, auth_headers: dict):
        """Test status for non-existent receipt"""
        response = client.get("/api/v1/receipts/99999/status", headers=auth_headers)
        assert response.status_code == 404


class TestReceiptList:
    """Tests for receipt listing"""
    
    def test_list_empty(self, client: TestClient, auth_headers: dict):
        """Test listing when no receipts"""
        response = client.get("/api/v1/receipts/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
    
    def test_list_with_receipts(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test listing multiple receipts"""
        receipts = [
            Receipt(
                user_id=test_user.id,
                original_filename=f"test{i}.jpg",
                file_url=f"https://s3.amazonaws.com/test{i}.jpg",
                status=ReceiptStatus.APPROVED,
                total_amount=100.0 * i
            )
            for i in range(1, 4)
        ]
        db.add_all(receipts)
        db.commit()
        
        response = client.get("/api/v1/receipts/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 3
    
    def test_list_pagination(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test pagination"""
        receipts = [
            Receipt(
                user_id=test_user.id,
                original_filename=f"test{i}.jpg",
                file_url=f"https://s3.amazonaws.com/test{i}.jpg",
                status=ReceiptStatus.APPROVED
            )
            for i in range(25)
        ]
        db.add_all(receipts)
        db.commit()
        
        response = client.get("/api/v1/receipts/?page=1&page_size=10", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] >= 25
        assert data["page"] == 1
    
    def test_filter_by_status(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test status filter"""
        approved = Receipt(
            user_id=test_user.id,
            original_filename="approved.jpg",
            file_url="https://s3.amazonaws.com/approved.jpg",
            status=ReceiptStatus.APPROVED
        )
        review = Receipt(
            user_id=test_user.id,
            original_filename="review.jpg",
            file_url="https://s3.amazonaws.com/review.jpg",
            status=ReceiptStatus.REVIEW
        )
        db.add_all([approved, review])
        db.commit()
        
        response = client.get("/api/v1/receipts/?status=approved", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert all(item["status"] == "approved" for item in data["items"])
    
    def test_filter_by_date_range(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test date range filter"""
        today = datetime.utcnow()
        yesterday = today - timedelta(days=1)
        last_week = today - timedelta(days=7)
        
        receipts = [
            Receipt(
                user_id=test_user.id,
                original_filename="recent.jpg",
                file_url="https://s3.amazonaws.com/recent.jpg",
                status=ReceiptStatus.APPROVED,
                receipt_date=yesterday
            ),
            Receipt(
                user_id=test_user.id,
                original_filename="old.jpg",
                file_url="https://s3.amazonaws.com/old.jpg",
                status=ReceiptStatus.APPROVED,
                receipt_date=last_week
            )
        ]
        db.add_all(receipts)
        db.commit()
        
        response = client.get(
            f"/api/v1/receipts/?date_from={yesterday.isoformat()}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 1
    
    def test_filter_by_category(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test category filter"""
        cat1 = Category(name_he="מזון", name_en="Food", icon="🍔")
        cat2 = Category(name_he="דלק", name_en="Fuel", icon="⛽")
        db.add_all([cat1, cat2])
        db.commit()
        
        receipts = [
            Receipt(
                user_id=test_user.id,
                original_filename="food.jpg",
                file_url="https://s3.amazonaws.com/food.jpg",
                status=ReceiptStatus.APPROVED,
                category_id=cat1.id
            ),
            Receipt(
                user_id=test_user.id,
                original_filename="fuel.jpg",
                file_url="https://s3.amazonaws.com/fuel.jpg",
                status=ReceiptStatus.APPROVED,
                category_id=cat2.id
            )
        ]
        db.add_all(receipts)
        db.commit()
        
        response = client.get(f"/api/v1/receipts/?category_ids={cat1.id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert all(
            item["category_id"] == cat1.id 
            for item in data["items"] 
            if item.get("category_id")
        )
    
    def test_filter_by_amount_range(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test amount filter"""
        receipts = [
            Receipt(
                user_id=test_user.id,
                original_filename="cheap.jpg",
                file_url="https://s3.amazonaws.com/cheap.jpg",
                status=ReceiptStatus.APPROVED,
                total_amount=50.0
            ),
            Receipt(
                user_id=test_user.id,
                original_filename="expensive.jpg",
                file_url="https://s3.amazonaws.com/expensive.jpg",
                status=ReceiptStatus.APPROVED,
                total_amount=500.0
            )
        ]
        db.add_all(receipts)
        db.commit()
        
        response = client.get(
            "/api/v1/receipts/?amount_min=100&amount_max=1000",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        for item in data["items"]:
            if item.get("total_amount"):
                assert 100 <= item["total_amount"] <= 1000
    
    def test_search_by_vendor(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test search query"""
        receipts = [
            Receipt(
                user_id=test_user.id,
                original_filename="test.jpg",
                file_url="https://s3.amazonaws.com/test.jpg",
                status=ReceiptStatus.APPROVED,
                vendor_name="סופר פארם"
            ),
            Receipt(
                user_id=test_user.id,
                original_filename="test2.jpg",
                file_url="https://s3.amazonaws.com/test2.jpg",
                status=ReceiptStatus.APPROVED,
                vendor_name="רמי לוי"
            )
        ]
        db.add_all(receipts)
        db.commit()
        
        response = client.get("/api/v1/receipts/?search_query=פארם", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 1
    
    def test_sort_by_amount_desc(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test sorting"""
        receipts = [
            Receipt(
                user_id=test_user.id,
                original_filename="low.jpg",
                file_url="https://s3.amazonaws.com/low.jpg",
                status=ReceiptStatus.APPROVED,
                total_amount=100.0
            ),
            Receipt(
                user_id=test_user.id,
                original_filename="high.jpg",
                file_url="https://s3.amazonaws.com/high.jpg",
                status=ReceiptStatus.APPROVED,
                total_amount=500.0
            )
        ]
        db.add_all(receipts)
        db.commit()
        
        response = client.get(
            "/api/v1/receipts/?sort_by=total_amount&sort_order=desc",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        if len(data["items"]) >= 2:
            amounts = [item["total_amount"] for item in data["items"] if item.get("total_amount")]
            if len(amounts) >= 2:
                assert amounts[0] >= amounts[1]


class TestReceiptCRUD:
    """Tests for get, update, delete operations"""
    
    def test_get_receipt_success(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test getting specific receipt"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/test.jpg",
            status=ReceiptStatus.APPROVED,
            vendor_name="Test Vendor",
            total_amount=150.0
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        
        response = client.get(f"/api/v1/receipts/{receipt.id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == receipt.id
        assert data["vendor_name"] == "Test Vendor"
    
    def test_get_receipt_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting non-existent receipt"""
        response = client.get("/api/v1/receipts/99999", headers=auth_headers)
        assert response.status_code == 404
    
    def test_get_other_users_receipt(self, client: TestClient, auth_headers: dict, db):
        """Test accessing another user's receipt"""
        from app.models.user import User
        other_user = User(
            email="other@example.com",
            full_name="Other User",
            id_number="305219892",
            phone_number="0501234567"
        )
        db.add(other_user)
        db.commit()
        
        receipt = Receipt(
            user_id=other_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/test.jpg",
            status=ReceiptStatus.APPROVED
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        
        response = client.get(f"/api/v1/receipts/{receipt.id}", headers=auth_headers)
        assert response.status_code == 404
    
    def test_update_receipt_success(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test updating receipt"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/test.jpg",
            status=ReceiptStatus.REVIEW,
            vendor_name="Old Vendor",
            total_amount=100.0
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        
        update_data = {
            "vendor_name": "New Vendor",
            "total_amount": 150.0
        }
        
        response = client.patch(
            f"/api/v1/receipts/{receipt.id}",
            headers=auth_headers,
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["vendor_name"] == "New Vendor"
        assert data["total_amount"] == 150.0
    
    def test_update_with_validation(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test update with validated fields"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/test.jpg",
            status=ReceiptStatus.REVIEW
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        
        update_data = {
            "business_number": "123456783",  # Valid Luhn
            "receipt_number": "12345",
            "pre_vat_amount": 100.0,
            "vat_amount": 17.0,
            "total_amount": 117.0
        }
        
        response = client.patch(
            f"/api/v1/receipts/{receipt.id}",
            headers=auth_headers,
            json=update_data
        )
        
        assert response.status_code == 200
    
    def test_update_not_found(self, client: TestClient, auth_headers: dict):
        """Test updating non-existent receipt"""
        response = client.patch(
            "/api/v1/receipts/99999",
            headers=auth_headers,
            json={"vendor_name": "New"}
        )
        assert response.status_code == 404
    
    def test_delete_receipt_success(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test deleting receipt"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/test.jpg",
            status=ReceiptStatus.APPROVED
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        receipt_id = receipt.id
        
        response = client.delete(f"/api/v1/receipts/{receipt_id}", headers=auth_headers)
        
        assert response.status_code == 204
        
        # Verify deletion
        deleted = db.query(Receipt).filter(Receipt.id == receipt_id).first()
        assert deleted is None
    
    def test_delete_not_found(self, client: TestClient, auth_headers: dict):
        """Test deleting non-existent receipt"""
        response = client.delete("/api/v1/receipts/99999", headers=auth_headers)
        assert response.status_code == 404


class TestReceiptApproval:
    """Tests for receipt approval"""
    
    def test_approve_success(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test approving receipt"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/test.jpg",
            status=ReceiptStatus.REVIEW,
            vendor_name="Test Vendor",
            total_amount=100.0
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        
        response = client.post(
            f"/api/v1/receipts/{receipt.id}/approve",
            headers=auth_headers,
            json={}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "approved"
    
    def test_approve_not_in_review(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test approving non-review receipt"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/test.jpg",
            status=ReceiptStatus.PROCESSING
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        
        response = client.post(
            f"/api/v1/receipts/{receipt.id}/approve",
            headers=auth_headers,
            json={}
        )
        
        assert response.status_code in [400, 409]


class TestReceiptDuplicates:
    """Tests for duplicate detection"""
    
    def test_check_duplicate_found(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test duplicate detection - duplicate found"""
        existing = Receipt(
            user_id=test_user.id,
            original_filename="original.jpg",
            file_url="https://s3.amazonaws.com/original.jpg",
            status=ReceiptStatus.APPROVED,
            vendor_name="Test Vendor",
            receipt_number="12345",
            receipt_date=datetime.utcnow(),
            total_amount=100.0
        )
        db.add(existing)
        db.commit()
        
        check_data = {
            "vendor_name": "Test Vendor",
            "receipt_number": "12345",
            "receipt_date": datetime.utcnow().isoformat(),
            "total_amount": 100.0
        }
        
        response = client.post(
            "/api/v1/receipts/check-duplicate",
            headers=auth_headers,
            json=check_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "is_duplicate" in data
    
    def test_check_duplicate_not_found(self, client: TestClient, auth_headers: dict, db):
        """Test duplicate detection - no duplicate"""
        check_data = {
            "vendor_name": "Unique Vendor",
            "receipt_number": "UNIQUE123",
            "receipt_date": datetime.utcnow().isoformat(),
            "total_amount": 999.99
        }
        
        response = client.post(
            "/api/v1/receipts/check-duplicate",
            headers=auth_headers,
            json=check_data
        )
        
        assert response.status_code == 200


class TestReceiptSearch:
    """Tests for search functionality"""
    
    def test_search_by_vendor(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test searching by vendor name"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="searchable.jpg",
            file_url="https://s3.amazonaws.com/searchable.jpg",
            status=ReceiptStatus.APPROVED,
            vendor_name="Unique Vendor Name",
            receipt_number="SEARCH123"
        )
        db.add(receipt)
        db.commit()
        
        response = client.get("/api/v1/receipts/search?q=Unique", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "results" in data or "items" in data


class TestReceiptHistory:
    """Tests for edit history"""
    
    def test_get_history(self, client: TestClient, auth_headers: dict, db, test_user):
        """Test getting receipt edit history"""
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="test.jpg",
            file_url="https://s3.amazonaws.com/test.jpg",
            status=ReceiptStatus.APPROVED,
            vendor_name="Original Vendor"
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        
        # Create edit
        edit = ReceiptEdit(
            receipt_id=receipt.id,
            user_id=test_user.id,
            field_name="vendor_name",
            old_value="Original Vendor",
            new_value="Updated Vendor",
            edit_type="update"
        )
        db.add(edit)
        db.commit()
        
        response = client.get(f"/api/v1/receipts/{receipt.id}/history", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "edits" in data or isinstance(data, list)
