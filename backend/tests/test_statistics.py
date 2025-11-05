import pytest
from fastapi import status
from datetime import datetime, timedelta

def test_dashboard_statistics(client, auth_headers, test_user, db):
    """Test dashboard statistics"""
    from app.models.receipt import Receipt
    
    # Create test receipts
    today = datetime.utcnow()
    receipts = [
        Receipt(user_id=test_user.id, vendor_name="Vendor1", total_amount=100.0, 
                status="approved", date=today),
        Receipt(user_id=test_user.id, vendor_name="Vendor2", total_amount=200.0, 
                status="approved", date=today),
        Receipt(user_id=test_user.id, vendor_name="Vendor3", total_amount=150.0, 
                status="pending", date=today)
    ]
    db.add_all(receipts)
    db.commit()
    
    response = client.get("/api/v1/statistics/dashboard", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_receipts"] == 3
    assert data["approved_receipts"] == 2
    assert data["total_amount_approved"] == 300.0


def test_yearly_report(client, auth_headers, test_user, db):
    """Test yearly report generation"""
    from app.models.receipt import Receipt
    
    # Create receipts for different months
    today = datetime.utcnow()
    receipt1 = Receipt(
        user_id=test_user.id,
        vendor_name="Vendor1",
        total_amount=100.0,
        status="approved",
        date=today.replace(month=1, day=15)
    )
    receipt2 = Receipt(
        user_id=test_user.id,
        vendor_name="Vendor2",
        total_amount=200.0,
        status="approved",
        date=today.replace(month=2, day=20)
    )
    db.add_all([receipt1, receipt2])
    db.commit()
    
    response = client.get(
        "/api/v1/statistics/yearly",
        headers=auth_headers,
        params={"year": today.year}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "monthly_breakdown" in data
    assert data["total_amount"] == 300.0


def test_category_breakdown(client, auth_headers, test_user, test_categories, db):
    """Test category breakdown statistics"""
    from app.models.receipt import Receipt
    
    receipt1 = Receipt(
        user_id=test_user.id,
        vendor_name="Vendor1",
        total_amount=100.0,
        category_id=test_categories[0].id,
        status="approved"
    )
    receipt2 = Receipt(
        user_id=test_user.id,
        vendor_name="Vendor2",
        total_amount=200.0,
        category_id=test_categories[0].id,
        status="approved"
    )
    db.add_all([receipt1, receipt2])
    db.commit()
    
    response = client.get("/api/v1/statistics/dashboard", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "category_breakdown" in data
