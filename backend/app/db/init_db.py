"""
Database initialization script
Creates all tables and seeds initial data
"""

from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.models.receipt import Receipt
from app.models.category import Category
from app.models.receipt_edit import ReceiptEdit
from app.models.subscription import Subscription


def init_db(db: Session) -> None:
    """
    Initialize database with tables and seed data
    
    Args:
        db: Database session
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Seed default categories
    default_categories = [
        {"name": "משרד", "name_en": "Office", "icon": "briefcase", "color": "#2563EB"},
        {"name": "שיווק", "name_en": "Marketing", "icon": "megaphone", "color": "#7C3AED"},
        {"name": "נסיעות", "name_en": "Travel", "icon": "car", "color": "#059669"},
        {"name": "ארוחות", "name_en": "Meals", "icon": "utensils", "color": "#DC2626"},
        {"name": "אירוח", "name_en": "Hospitality", "icon": "coffee", "color": "#EA580C"},
        {"name": "ציוד", "name_en": "Equipment", "icon": "package", "color": "#0891B2"},
        {"name": "שכר דירה", "name_en": "Rent", "icon": "home", "color": "#DB2777"},
        {"name": "תקשורת", "name_en": "Communication", "icon": "phone", "color": "#65A30D"},
        {"name": "משפטי", "name_en": "Legal", "icon": "scale", "color": "#CA8A04"},
        {"name": "ביטוח", "name_en": "Insurance", "icon": "shield", "color": "#475569"},
        {"name": "בריאות", "name_en": "Health", "icon": "heart", "color": "#EC4899"},
        {"name": "חינוך", "name_en": "Education", "icon": "book", "color": "#8B5CF6"},
        {"name": "אחר", "name_en": "Other", "icon": "more-horizontal", "color": "#6B7280"},
    ]
    
    # Check if categories already exist
    existing = db.query(Category).first()
    if not existing:
        for cat_data in default_categories:
            category = Category(**cat_data)
            db.add(category)
        db.commit()
        print("✅ Default categories created")


if __name__ == "__main__":
    from app.db.session import SessionLocal
    
    print("🔄 Initializing database...")
    db = SessionLocal()
    
    try:
        init_db(db)
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise
    finally:
        db.close()
