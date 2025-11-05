import pytest
from fastapi import status
from io import BytesIO

def test_upload_receipt_success(client, auth_headers, test_categories):
    """Test successful receipt upload"""
    # Create fake image file
    image_file = BytesIO(b"fake image content")
    
    response = client.post(
        "/api/v1/receipts/upload",
        headers=auth_headers,
        files={"file": ("receipt.jpg", image_file, "image/jpeg")}
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["status"] == "processing"


def test_upload_receipt_no_auth(client):
    """Test receipt upload without authentication"""
    image_file = BytesIO(b"fake image content")
    
    response = client.post(
        "/api/v1/receipts/upload",
        files={"file": ("receipt.jpg", image_file, "image/jpeg")}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_upload_receipt_invalid_file(client, auth_headers):
    """Test upload with invalid file type"""
    text_file = BytesIO(b"not an image")
    
    response = client.post(
        "/api/v1/receipts/upload",
        headers=auth_headers,
        files={"file": ("document.txt", text_file, "text/plain")}
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_receipts(client, auth_headers, test_user, db):
    """Test listing receipts"""
    # Create test receipt
    from app.models.receipt import Receipt
    receipt = Receipt(
        user_id=test_user.id,
        vendor_name="Test Vendor",
        total_amount=100.0,
        status="approved"
    )
    db.add(receipt)
    db.commit()
    
    response = client.get("/api/v1/receipts", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["receipts"]) > 0


def test_get_receipt(client, auth_headers, test_user, db):
    """Test getting single receipt"""
    from app.models.receipt import Receipt
    receipt = Receipt(
        user_id=test_user.id,
        vendor_name="Test Vendor",
        total_amount=100.0
    )
    db.add(receipt)
    db.commit()
    
    response = client.get(f"/api/v1/receipts/{receipt.id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == receipt.id
    assert data["vendor_name"] == "Test Vendor"


def test_get_receipt_not_found(client, auth_headers):
    """Test getting non-existent receipt"""
    response = client.get("/api/v1/receipts/99999", headers=auth_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_receipt(client, auth_headers, test_user, db):
    """Test updating receipt"""
    from app.models.receipt import Receipt
    receipt = Receipt(
        user_id=test_user.id,
        vendor_name="Old Vendor",
        total_amount=100.0
    )
    db.add(receipt)
    db.commit()
    
    response = client.put(
        f"/api/v1/receipts/{receipt.id}",
        headers=auth_headers,
        json={"vendor_name": "New Vendor"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["vendor_name"] == "New Vendor"


def test_approve_receipt(client, auth_headers, test_user, db):
    """Test approving receipt"""
    from app.models.receipt import Receipt
    receipt = Receipt(
        user_id=test_user.id,
        vendor_name="Test Vendor",
        total_amount=100.0,
        status="pending"
    )
    db.add(receipt)
    db.commit()
    
    response = client.post(
        f"/api/v1/receipts/{receipt.id}/approve",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "approved"


def test_delete_receipt(client, auth_headers, test_user, db):
    """Test deleting receipt"""
    from app.models.receipt import Receipt
    receipt = Receipt(
        user_id=test_user.id,
        vendor_name="Test Vendor",
        total_amount=100.0
    )
    db.add(receipt)
    db.commit()
    receipt_id = receipt.id
    
    response = client.delete(
        f"/api/v1/receipts/{receipt_id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify deleted
    get_response = client.get(f"/api/v1/receipts/{receipt_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_search_receipts(client, auth_headers, test_user, db):
    """Test receipt search"""
    from app.models.receipt import Receipt
    receipt1 = Receipt(user_id=test_user.id, vendor_name="סופר-פארם", total_amount=100.0)
    receipt2 = Receipt(user_id=test_user.id, vendor_name="רמי לוי", total_amount=200.0)
    db.add_all([receipt1, receipt2])
    db.commit()
    
    response = client.get(
        "/api/v1/receipts/search",
        headers=auth_headers,
        params={"q": "סופר"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["vendor_name"] == "סופר-פארם"
