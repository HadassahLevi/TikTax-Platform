"""
Database initialization script
Creates all tables and seeds initial data (categories, test user)
"""

from sqlalchemy.orm import Session
from datetime import datetime

from app.db.base import Base
from app.db.session import engine
from app.models.user import User, SubscriptionPlan
from app.models.receipt import Receipt
from app.models.category import Category
from app.models.receipt_edit import ReceiptEdit
from app.core.security import get_password_hash


def create_default_categories(db: Session) -> None:
    """
    Create 13 default Hebrew expense categories.
    
    Categories are based on common Israeli business expenses.
    Only creates if database is empty.
    """
    # Check if categories already exist
    existing = db.query(Category).first()
    if existing:
        print("⏭️  Categories already exist, skipping...")
        return
    
    default_categories = [
        {"name_hebrew": "משרד", "name_english": "Office", "icon": "briefcase", "color": "#2563EB", "sort_order": 1},
        {"name_hebrew": "שיווק", "name_english": "Marketing", "icon": "megaphone", "color": "#7C3AED", "sort_order": 2},
        {"name_hebrew": "נסיעות", "name_english": "Travel", "icon": "car", "color": "#059669", "sort_order": 3},
        {"name_hebrew": "ארוחות", "name_english": "Meals", "icon": "utensils", "color": "#DC2626", "sort_order": 4},
        {"name_hebrew": "אירוח", "name_english": "Hospitality", "icon": "coffee", "color": "#EA580C", "sort_order": 5},
        {"name_hebrew": "ציוד", "name_english": "Equipment", "icon": "package", "color": "#0891B2", "sort_order": 6},
        {"name_hebrew": "שכר דירה", "name_english": "Rent", "icon": "home", "color": "#DB2777", "sort_order": 7},
        {"name_hebrew": "תקשורת", "name_english": "Communication", "icon": "phone", "color": "#65A30D", "sort_order": 8},
        {"name_hebrew": "משפטי", "name_english": "Legal", "icon": "scale", "color": "#CA8A04", "sort_order": 9},
        {"name_hebrew": "ביטוח", "name_english": "Insurance", "icon": "shield", "color": "#475569", "sort_order": 10},
        {"name_hebrew": "בריאות", "name_english": "Health", "icon": "heart", "color": "#EC4899", "sort_order": 11},
        {"name_hebrew": "חינוך", "name_english": "Education", "icon": "book-open", "color": "#8B5CF6", "sort_order": 12},
        {"name_hebrew": "אחר", "name_english": "Other", "icon": "more-horizontal", "color": "#6B7280", "sort_order": 13},
    ]
    
    for cat_data in default_categories:
        category = Category(**cat_data, is_default=True)
        db.add(category)
    
    db.commit()
    print(f"✅ Created {len(default_categories)} default categories")


def create_test_user(db: Session) -> None:
    """
    Create a test user for development.
    
    WARNING: Only use in development environment!
    Credentials: test@tiktax.co.il / Test123456!
    """
    # Check if test user already exists
    existing = db.query(User).filter(User.email == "test@tiktax.co.il").first()
    if existing:
        print("⏭️  Test user already exists, skipping...")
        return
    
    test_user = User(
        email="test@tiktax.co.il",
        hashed_password=get_password_hash("Test123456!"),
        full_name="משתמש בדיקה",
        id_number="123456789",
        phone_number="+972501234567",
        is_phone_verified=True,
        is_email_verified=True,
        business_name="עסק בדיקה בע״מ",
        business_number="514567890",
        business_type="חברה בע״מ",
        subscription_plan=SubscriptionPlan.PRO,
        subscription_start_date=datetime.utcnow(),
        receipt_limit=1000,
        is_active=True,
    )
    
    db.add(test_user)
    db.commit()
    print("✅ Created test user (test@tiktax.co.il / Test123456!)")


def init_db(db: Session, create_test_data: bool = False) -> None:
    """
    Initialize database with tables and seed data.
    
    Args:
        db: Database session
        create_test_data: If True, creates test user (development only)
    """
    print("🔄 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")
    
    print("🔄 Seeding default categories...")
    create_default_categories(db)
    
    if create_test_data:
        print("🔄 Creating test user...")
        create_test_user(db)
    
    print("✅ Database initialization complete!")


if __name__ == "__main__":
    from app.db.session import SessionLocal
    import sys
    
    # Check if --with-test-data flag is passed
    create_test_data = "--with-test-data" in sys.argv
    
    print("� Tik-Tax Database Initialization")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        init_db(db, create_test_data=create_test_data)
        print("=" * 50)
        print("✅ Success! Database is ready to use.")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise
    finally:
        db.close()

