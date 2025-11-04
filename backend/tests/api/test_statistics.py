"""
Unit Tests for Statistics Endpoints
Tests dashboard analytics, yearly reports, and category statistics
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.user import User, SubscriptionPlan
from app.models.receipt import Receipt, ReceiptStatus
from app.models.category import Category


class TestDashboardStatistics:
    """Test dashboard statistics endpoint"""
    
    def test_dashboard_stats_empty_user(self, client, test_user_token):
        """Test dashboard stats for user with no receipts"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/v1/statistics/dashboard", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify zero values
        assert data["total_receipts"] == 0
        assert data["approved_receipts"] == 0
        assert data["pending_receipts"] == 0
        assert data["monthly_receipts"] == 0
        assert data["monthly_amount"] == 0
        assert data["monthly_average"] == 0
        assert data["categories"] == []
        assert data["recent_receipts"] == []
        assert data["monthly_trend"] == []
        
        # Verify subscription usage
        assert data["receipts_limit"] == 50  # Default FREE plan
        assert data["receipts_used"] == 0
        assert data["receipts_remaining"] == 50
        assert data["usage_percentage"] == 0
    
    def test_dashboard_stats_with_receipts(self, client, test_user_token, db: Session, test_user: User):
        """Test dashboard stats with multiple receipts"""
        # Create test category
        category = Category(
            name_hebrew="משרד",
            name_english="Office",
            icon="briefcase",
            color="#2563EB",
            is_default=True
        )
        db.add(category)
        db.commit()
        
        # Create receipts for current month
        now = datetime.utcnow()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        receipts = []
        for i in range(5):
            receipt = Receipt(
                user_id=test_user.id,
                original_filename=f"receipt_{i}.jpg",
                file_url=f"https://s3.example.com/receipt_{i}.jpg",
                file_size=1024 * (i + 1),
                mime_type="image/jpeg",
                vendor_name=f"Vendor {i}",
                receipt_date=current_month_start + timedelta(days=i),
                total_amount=100.0 * (i + 1),
                vat_amount=17.0 * (i + 1),
                category_id=category.id,
                status=ReceiptStatus.APPROVED,
                approved_at=now
            )
            receipts.append(receipt)
            db.add(receipt)
        
        # Create receipts for previous month
        prev_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        for i in range(3):
            receipt = Receipt(
                user_id=test_user.id,
                original_filename=f"prev_receipt_{i}.jpg",
                file_url=f"https://s3.example.com/prev_receipt_{i}.jpg",
                file_size=1024,
                mime_type="image/jpeg",
                vendor_name=f"Prev Vendor {i}",
                receipt_date=prev_month_start + timedelta(days=i),
                total_amount=50.0 * (i + 1),
                vat_amount=8.5 * (i + 1),
                category_id=category.id,
                status=ReceiptStatus.APPROVED,
                approved_at=prev_month_start
            )
            db.add(receipt)
        
        # Create pending receipt
        pending_receipt = Receipt(
            user_id=test_user.id,
            original_filename="pending.jpg",
            file_url="https://s3.example.com/pending.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            status=ReceiptStatus.REVIEW
        )
        db.add(pending_receipt)
        
        db.commit()
        
        # Get dashboard stats
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/v1/statistics/dashboard", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify counts
        assert data["total_receipts"] == 9  # 5 + 3 + 1
        assert data["approved_receipts"] == 8
        assert data["pending_receipts"] == 1
        
        # Verify current month (5 receipts: 100, 200, 300, 400, 500 = 1500)
        assert data["monthly_receipts"] == 5
        assert data["monthly_amount"] == 1500.0
        assert data["monthly_average"] == 300.0
        
        # Verify previous month (3 receipts: 50, 100, 150 = 300)
        assert data["prev_monthly_receipts"] == 3
        assert data["prev_monthly_amount"] == 300.0
        
        # Verify percentage changes
        # Receipts: (5 - 3) / 3 * 100 = 66.67%
        assert abs(data["receipts_change_percent"] - 66.67) < 0.1
        # Amount: (1500 - 300) / 300 * 100 = 400%
        assert abs(data["amount_change_percent"] - 400.0) < 0.1
        
        # Verify categories
        assert len(data["categories"]) == 1
        assert data["categories"][0]["category_name"] == "משרד"
        assert data["categories"][0]["count"] == 8
        assert data["categories"][0]["total_amount"] == 1800.0  # 1500 + 300
        assert data["categories"][0]["percentage"] == 100.0
        
        # Verify recent receipts (last 5 approved)
        assert len(data["recent_receipts"]) == 5
        assert data["recent_receipts"][0]["vendor_name"] == "Vendor 4"
        
        # Verify monthly trend
        assert len(data["monthly_trend"]) > 0
    
    def test_dashboard_division_by_zero_handling(self, client, test_user_token, db: Session, test_user: User):
        """Test that division by zero is handled gracefully"""
        # Create only pending receipts (no approved ones)
        receipt = Receipt(
            user_id=test_user.id,
            original_filename="pending.jpg",
            file_url="https://s3.example.com/pending.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            status=ReceiptStatus.PROCESSING
        )
        db.add(receipt)
        db.commit()
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/v1/statistics/dashboard", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should handle zero approved receipts gracefully
        assert data["monthly_average"] == 0
        assert data["receipts_change_percent"] == 0
        assert data["amount_change_percent"] == 0


class TestYearlyReport:
    """Test yearly report endpoint"""
    
    def test_yearly_report_default_current_year(self, client, test_user_token):
        """Test yearly report defaults to current year"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/v1/statistics/yearly", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        current_year = datetime.utcnow().year
        assert data["year"] == current_year
        assert data["total_receipts"] == 0
        assert data["total_amount"] == 0
        assert data["total_vat"] == 0
        assert data["categories"] == []
        assert data["monthly_breakdown"] == []
    
    def test_yearly_report_specific_year(self, client, test_user_token, db: Session, test_user: User):
        """Test yearly report for specific year"""
        # Create category
        category = Category(
            name_hebrew="משרד",
            name_english="Office",
            icon="briefcase",
            color="#2563EB"
        )
        db.add(category)
        db.commit()
        
        # Create receipts for 2024
        year_2024 = 2024
        for month in range(1, 13):  # All 12 months
            receipt = Receipt(
                user_id=test_user.id,
                original_filename=f"receipt_{month}.jpg",
                file_url=f"https://s3.example.com/receipt_{month}.jpg",
                file_size=1024,
                mime_type="image/jpeg",
                vendor_name=f"Vendor {month}",
                receipt_date=datetime(year_2024, month, 15),
                total_amount=1000.0,
                vat_amount=170.0,
                category_id=category.id,
                status=ReceiptStatus.APPROVED,
                approved_at=datetime(year_2024, month, 15)
            )
            db.add(receipt)
        
        db.commit()
        
        # Get yearly report
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get(f"/api/v1/statistics/yearly?year={year_2024}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["year"] == year_2024
        assert data["total_receipts"] == 12
        assert data["total_amount"] == 12000.0
        assert data["total_vat"] == 2040.0
        
        # Verify category breakdown
        assert len(data["categories"]) == 1
        assert data["categories"][0]["total_amount"] == 12000.0
        
        # Verify monthly breakdown (all 12 months)
        assert len(data["monthly_breakdown"]) == 12
        for i, month_data in enumerate(data["monthly_breakdown"], start=1):
            assert month_data["month"] == f"{year_2024}-{i:02d}"
            assert month_data["total_receipts"] == 1
            assert month_data["total_amount"] == 1000.0
    
    def test_yearly_report_invalid_year(self, client, test_user_token):
        """Test yearly report with invalid year"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        
        # Year too old
        response = client.get("/api/v1/statistics/yearly?year=1999", headers=headers)
        assert response.status_code == 400
        
        # Year too far in future
        response = client.get("/api/v1/statistics/yearly?year=2101", headers=headers)
        assert response.status_code == 400
    
    def test_yearly_report_no_data(self, client, test_user_token, db: Session, test_user: User):
        """Test yearly report with no receipts for year"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/v1/statistics/yearly?year=2020", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["year"] == 2020
        assert data["total_receipts"] == 0
        assert data["total_amount"] == 0
        assert data["total_vat"] == 0
        assert data["categories"] == []
        assert data["monthly_breakdown"] == []


class TestCategoryStatistics:
    """Test category-specific statistics endpoint"""
    
    def test_category_stats_basic(self, client, test_user_token, db: Session, test_user: User):
        """Test basic category statistics"""
        # Create category
        category = Category(
            name_hebrew="משרד",
            name_english="Office",
            icon="briefcase",
            color="#2563EB"
        )
        db.add(category)
        db.commit()
        
        # Create receipts
        for i in range(5):
            receipt = Receipt(
                user_id=test_user.id,
                original_filename=f"receipt_{i}.jpg",
                file_url=f"https://s3.example.com/receipt_{i}.jpg",
                file_size=1024,
                mime_type="image/jpeg",
                vendor_name=f"Vendor {i}",
                receipt_date=datetime(2024, 1, i + 1),
                total_amount=100.0 * (i + 1),
                category_id=category.id,
                status=ReceiptStatus.APPROVED
            )
            db.add(receipt)
        
        db.commit()
        
        # Get category stats
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get(f"/api/v1/statistics/category/{category.id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["category_id"] == category.id
        assert data["category_name"] == "משרד"
        assert data["count"] == 5
        assert data["total_amount"] == 1500.0  # 100 + 200 + 300 + 400 + 500
        assert data["percentage"] == 100.0  # Only category
    
    def test_category_stats_with_year_filter(self, client, test_user_token, db: Session, test_user: User):
        """Test category statistics filtered by year"""
        category = Category(
            name_hebrew="משרד",
            name_english="Office",
            icon="briefcase",
            color="#2563EB"
        )
        db.add(category)
        db.commit()
        
        # Create receipts in different years
        receipt_2024 = Receipt(
            user_id=test_user.id,
            original_filename="receipt_2024.jpg",
            file_url="https://s3.example.com/receipt_2024.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            receipt_date=datetime(2024, 6, 15),
            total_amount=1000.0,
            category_id=category.id,
            status=ReceiptStatus.APPROVED
        )
        receipt_2023 = Receipt(
            user_id=test_user.id,
            original_filename="receipt_2023.jpg",
            file_url="https://s3.example.com/receipt_2023.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            receipt_date=datetime(2023, 6, 15),
            total_amount=500.0,
            category_id=category.id,
            status=ReceiptStatus.APPROVED
        )
        db.add_all([receipt_2024, receipt_2023])
        db.commit()
        
        # Get stats for 2024 only
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get(f"/api/v1/statistics/category/{category.id}?year=2024", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["count"] == 1
        assert data["total_amount"] == 1000.0
    
    def test_category_stats_with_month_filter(self, client, test_user_token, db: Session, test_user: User):
        """Test category statistics filtered by year and month"""
        category = Category(
            name_hebrew="משרד",
            name_english="Office",
            icon="briefcase",
            color="#2563EB"
        )
        db.add(category)
        db.commit()
        
        # Create receipts in different months
        receipt_jan = Receipt(
            user_id=test_user.id,
            original_filename="receipt_jan.jpg",
            file_url="https://s3.example.com/receipt_jan.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            receipt_date=datetime(2024, 1, 15),
            total_amount=1000.0,
            category_id=category.id,
            status=ReceiptStatus.APPROVED
        )
        receipt_feb = Receipt(
            user_id=test_user.id,
            original_filename="receipt_feb.jpg",
            file_url="https://s3.example.com/receipt_feb.jpg",
            file_size=1024,
            mime_type="image/jpeg",
            receipt_date=datetime(2024, 2, 15),
            total_amount=500.0,
            category_id=category.id,
            status=ReceiptStatus.APPROVED
        )
        db.add_all([receipt_jan, receipt_feb])
        db.commit()
        
        # Get stats for January only
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get(
            f"/api/v1/statistics/category/{category.id}?year=2024&month=1",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["count"] == 1
        assert data["total_amount"] == 1000.0
    
    def test_category_stats_not_found(self, client, test_user_token):
        """Test category statistics for non-existent category"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/v1/statistics/category/9999", headers=headers)
        
        assert response.status_code == 404


class TestStatisticsPerformance:
    """Test performance and optimization of statistics queries"""
    
    def test_dashboard_with_large_dataset(self, client, test_user_token, db: Session, test_user: User):
        """Test dashboard performance with large number of receipts"""
        # Create category
        category = Category(
            name_hebrew="משרד",
            name_english="Office",
            icon="briefcase",
            color="#2563EB"
        )
        db.add(category)
        db.commit()
        
        # Create 100 receipts
        receipts = []
        now = datetime.utcnow()
        for i in range(100):
            receipt = Receipt(
                user_id=test_user.id,
                original_filename=f"receipt_{i}.jpg",
                file_url=f"https://s3.example.com/receipt_{i}.jpg",
                file_size=1024,
                mime_type="image/jpeg",
                vendor_name=f"Vendor {i}",
                receipt_date=now - timedelta(days=i),
                total_amount=100.0,
                vat_amount=17.0,
                category_id=category.id,
                status=ReceiptStatus.APPROVED,
                approved_at=now
            )
            receipts.append(receipt)
        
        db.bulk_save_objects(receipts)
        db.commit()
        
        # Measure query time
        import time
        headers = {"Authorization": f"Bearer {test_user_token}"}
        
        start_time = time.time()
        response = client.get("/api/v1/statistics/dashboard", headers=headers)
        end_time = time.time()
        
        assert response.status_code == 200
        
        # Should complete in under 2 seconds even with 100 receipts
        query_time = end_time - start_time
        assert query_time < 2.0, f"Query took {query_time:.2f}s, expected < 2s"
        
        # Verify correct data
        data = response.json()
        assert data["total_receipts"] == 100
        assert len(data["recent_receipts"]) == 5  # Only 5 recent
        assert len(data["categories"]) <= 5  # Top 5 categories


class TestStatisticsEdgeCases:
    """Test edge cases and error handling"""
    
    def test_unauthorized_access(self, client):
        """Test that unauthenticated requests are rejected"""
        response = client.get("/api/v1/statistics/dashboard")
        assert response.status_code == 401
        
        response = client.get("/api/v1/statistics/yearly")
        assert response.status_code == 401
    
    def test_subscription_usage_calculation(self, client, test_user_token, db: Session, test_user: User):
        """Test subscription usage percentage calculation"""
        # Update user subscription
        test_user.receipt_limit = 100
        test_user.receipts_used_this_month = 75
        db.commit()
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/v1/statistics/dashboard", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["receipts_limit"] == 100
        assert data["receipts_used"] == 75
        assert data["receipts_remaining"] == 25
        assert data["usage_percentage"] == 75.0
    
    def test_negative_receipts_remaining_handled(self, client, test_user_token, db: Session, test_user: User):
        """Test that over-limit usage is handled correctly"""
        # User exceeded limit
        test_user.receipt_limit = 50
        test_user.receipts_used_this_month = 60
        db.commit()
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/v1/statistics/dashboard", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should show 0 remaining, not negative
        assert data["receipts_remaining"] == 0
        assert data["usage_percentage"] == 120.0
