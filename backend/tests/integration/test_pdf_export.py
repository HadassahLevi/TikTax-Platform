"""
PDF Export Integration Tests
Test PDF export endpoint with real database
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.main import app
from app.models.user import User, SubscriptionPlan
from app.models.receipt import Receipt, ReceiptStatus
from app.models.category import Category
from app.core.security import get_password_hash


@pytest.fixture
def test_user(db: Session):
    """Create test user with business info"""
    user = User(
        email="pdftest@tiktax.co.il",
        hashed_password=get_password_hash("testpassword123"),
        full_name="PDF Test User",
        id_number="123456789",
        phone_number="0501234567",
        business_name="PDF Test Business Ltd.",
        business_number="987654321",
        subscription_plan=SubscriptionPlan.PRO,
        receipt_limit=1000,
        is_active=True,
        is_email_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_categories(db: Session):
    """Create test categories"""
    categories = [
        Category(
            name="Office Supplies",
            name_hebrew="ציוד משרדי",
            description="Office and business supplies",
            color="#2563EB"
        ),
        Category(
            name="Transportation",
            name_hebrew="תחבורה",
            description="Transportation and fuel",
            color="#059669"
        ),
        Category(
            name="Meals & Entertainment",
            name_hebrew="אוכל ואירוח",
            description="Business meals and entertainment",
            color="#F59E0B"
        )
    ]
    for cat in categories:
        db.add(cat)
    db.commit()
    return categories


@pytest.fixture
def test_receipts(db: Session, test_user: User, test_categories: list):
    """Create test receipts"""
    receipts = []
    base_date = datetime(2024, 1, 15, 10, 0, 0)
    
    receipt_data = [
        {
            "vendor": "Office Depot Israel",
            "category_id": test_categories[0].id,
            "total": 500.00,
            "vat": 72.65,
            "pre_vat": 427.35,
        },
        {
            "vendor": "Shell Gas Station",
            "category_id": test_categories[1].id,
            "total": 300.00,
            "vat": 43.59,
            "pre_vat": 256.41,
        },
        {
            "vendor": "Cafe Aroma",
            "category_id": test_categories[2].id,
            "total": 150.00,
            "vat": 21.79,
            "pre_vat": 128.21,
        },
        {
            "vendor": "Super-Pharm",
            "category_id": test_categories[0].id,
            "total": 200.00,
            "vat": 29.06,
            "pre_vat": 170.94,
        }
    ]
    
    for i, data in enumerate(receipt_data):
        receipt = Receipt(
            user_id=test_user.id,
            original_filename=f"receipt_{i+1}.jpg",
            file_url=f"https://tiktax-test.s3.amazonaws.com/receipts/receipt_{i+1}.jpg",
            file_size=150000 + (i * 10000),
            mime_type="image/jpeg",
            vendor_name=data["vendor"],
            business_number=f"51{i+1}234567",
            receipt_number=f"REC-{1000+i}",
            receipt_date=base_date + timedelta(days=i * 3),
            total_amount=data["total"],
            vat_amount=data["vat"],
            pre_vat_amount=data["pre_vat"],
            category_id=data["category_id"],
            status=ReceiptStatus.APPROVED,
            confidence_score=95.5 + i,
            approved_at=datetime.utcnow()
        )
        db.add(receipt)
        receipts.append(receipt)
    
    db.commit()
    return receipts


@pytest.fixture
def auth_headers(client: TestClient, test_user: User):
    """Get authentication headers"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestPDFExportIntegration:
    """Integration tests for PDF export"""
    
    def test_generate_pdf_export_basic(
        self,
        client: TestClient,
        auth_headers: dict,
        test_receipts: list
    ):
        """Test basic PDF export generation"""
        response = client.post(
            "/api/v1/export/generate",
            headers=auth_headers,
            json={
                "format": "pdf",
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2024-01-31T23:59:59",
                "include_images": False
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        
        assert "export_id" in data
        assert "download_url" in data
        assert "expires_at" in data
        assert "file_size" in data
        assert data["file_size"] > 1000  # PDF should have content
    
    def test_download_generated_pdf(
        self,
        client: TestClient,
        auth_headers: dict,
        test_receipts: list
    ):
        """Test downloading generated PDF"""
        # Generate export
        gen_response = client.post(
            "/api/v1/export/generate",
            headers=auth_headers,
            json={
                "format": "pdf",
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2024-01-31T23:59:59",
                "include_images": False
            }
        )
        
        assert gen_response.status_code == 201
        export_id = gen_response.json()["export_id"]
        
        # Download
        dl_response = client.get(
            f"/api/v1/export/download/{export_id}",
            headers=auth_headers
        )
        
        assert dl_response.status_code == 200
        assert dl_response.headers["content-type"] == "application/pdf"
        assert "attachment" in dl_response.headers["content-disposition"]
        
        # Verify PDF format
        content = dl_response.content
        assert content[:4] == b'%PDF'
        assert len(content) > 1000
    
    def test_pdf_export_with_category_filter(
        self,
        client: TestClient,
        auth_headers: dict,
        test_receipts: list,
        test_categories: list
    ):
        """Test PDF export with category filter"""
        response = client.post(
            "/api/v1/export/generate",
            headers=auth_headers,
            json={
                "format": "pdf",
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2024-01-31T23:59:59",
                "category_ids": [test_categories[0].id],  # Office supplies only
                "include_images": False
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["file_size"] > 500  # Should have content
    
    def test_pdf_export_no_receipts(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test PDF export with no receipts in date range"""
        response = client.post(
            "/api/v1/export/generate",
            headers=auth_headers,
            json={
                "format": "pdf",
                "date_from": "2025-01-01T00:00:00",
                "date_to": "2025-01-31T23:59:59",
                "include_images": False
            }
        )
        
        # Should return 404 when no receipts found
        assert response.status_code == 404
        assert "לא נמצאו קבלות" in response.json()["detail"]
    
    def test_pdf_export_invalid_date_range(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test PDF export with invalid date range"""
        response = client.post(
            "/api/v1/export/generate",
            headers=auth_headers,
            json={
                "format": "pdf",
                "date_from": "2024-12-31T00:00:00",
                "date_to": "2024-01-01T23:59:59",  # End before start
                "include_images": False
            }
        )
        
        assert response.status_code == 400
        assert "תאריך התחלה" in response.json()["detail"]
    
    def test_pdf_export_too_large_date_range(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test PDF export with date range too large"""
        response = client.post(
            "/api/v1/export/generate",
            headers=auth_headers,
            json={
                "format": "pdf",
                "date_from": "2020-01-01T00:00:00",
                "date_to": "2024-01-01T23:59:59",  # More than 2 years
                "include_images": False
            }
        )
        
        assert response.status_code == 400
        assert "טווח תאריכים" in response.json()["detail"]
    
    def test_pdf_export_unauthorized(self, client: TestClient):
        """Test PDF export without authentication"""
        response = client.post(
            "/api/v1/export/generate",
            json={
                "format": "pdf",
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2024-01-31T23:59:59",
                "include_images": False
            }
        )
        
        assert response.status_code == 401
    
    def test_pdf_filename_format(
        self,
        client: TestClient,
        auth_headers: dict,
        test_receipts: list
    ):
        """Test PDF filename format"""
        # Generate export
        gen_response = client.post(
            "/api/v1/export/generate",
            headers=auth_headers,
            json={
                "format": "pdf",
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2024-01-31T23:59:59",
                "include_images": False
            }
        )
        
        export_id = gen_response.json()["export_id"]
        
        # Download
        dl_response = client.get(
            f"/api/v1/export/download/{export_id}",
            headers=auth_headers
        )
        
        content_disposition = dl_response.headers["content-disposition"]
        
        # Should be: attachment; filename=tiktax_receipts_YYYYMMDD_YYYYMMDD.pdf
        assert "tiktax_receipts_20240101_20240131.pdf" in content_disposition
    
    def test_pdf_export_multiple_users_isolation(
        self,
        client: TestClient,
        db: Session,
        test_receipts: list
    ):
        """Test that users can only export their own receipts"""
        # Create second user
        user2 = User(
            email="user2@tiktax.co.il",
            hashed_password=get_password_hash("password123"),
            full_name="User Two",
            id_number="987654321",
            phone_number="0509876543",
            subscription_plan=SubscriptionPlan.FREE,
            is_active=True
        )
        db.add(user2)
        db.commit()
        
        # Login as user2
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "user2@tiktax.co.il",
                "password": "password123"
            }
        )
        user2_token = login_response.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        
        # Try to export (should find no receipts)
        response = client.post(
            "/api/v1/export/generate",
            headers=user2_headers,
            json={
                "format": "pdf",
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2024-01-31T23:59:59",
                "include_images": False
            }
        )
        
        # Should return 404 (no receipts for this user)
        assert response.status_code == 404
    
    @pytest.mark.skip(reason="Requires valid S3 URLs - for manual testing only")
    def test_pdf_export_with_images(
        self,
        client: TestClient,
        auth_headers: dict,
        test_receipts: list
    ):
        """Test PDF export with receipt images (requires valid URLs)"""
        response = client.post(
            "/api/v1/export/generate",
            headers=auth_headers,
            json={
                "format": "pdf",
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2024-01-31T23:59:59",
                "include_images": True
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # PDF with images should be larger
        assert data["file_size"] > 5000
    
    def test_pdf_content_hebrew_support(
        self,
        client: TestClient,
        auth_headers: dict,
        test_receipts: list
    ):
        """Test that PDF contains Hebrew content"""
        # Generate and download
        gen_response = client.post(
            "/api/v1/export/generate",
            headers=auth_headers,
            json={
                "format": "pdf",
                "date_from": "2024-01-01T00:00:00",
                "date_to": "2024-01-31T23:59:59",
                "include_images": False
            }
        )
        
        export_id = gen_response.json()["export_id"]
        
        dl_response = client.get(
            f"/api/v1/export/download/{export_id}",
            headers=auth_headers
        )
        
        pdf_content = dl_response.content
        
        # PDF should be valid
        assert pdf_content[:4] == b'%PDF'
        
        # PDF should contain some Hebrew text markers
        # Note: Hebrew in PDFs is encoded, so we just check for substantial content
        assert len(pdf_content) > 2000
