"""add_stripe_fields_to_user

Revision ID: add_stripe_001
Revises: 
Create Date: 2025-11-07

Add Stripe integration fields to User model:
- stripe_customer_id: Stripe customer identifier
- stripe_subscription_id: Active subscription identifier
- subscription_status: Billing status tracking

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_stripe_001'
down_revision = None  # Update this with your latest migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add Stripe fields to users table"""
    # Add stripe_customer_id column
    op.add_column('users', sa.Column('stripe_customer_id', sa.String(length=255), nullable=True))
    op.create_index('ix_users_stripe_customer_id', 'users', ['stripe_customer_id'], unique=True)
    
    # Add stripe_subscription_id column
    op.add_column('users', sa.Column('stripe_subscription_id', sa.String(length=255), nullable=True))
    op.create_index('ix_users_stripe_subscription_id', 'users', ['stripe_subscription_id'], unique=False)
    
    # Add subscription_status column (modify existing if needed, or add new)
    # Check if column exists first
    op.add_column('users', sa.Column('subscription_status', sa.String(length=50), nullable=False, server_default='active'))


def downgrade() -> None:
    """Remove Stripe fields from users table"""
    # Drop indexes
    op.drop_index('ix_users_stripe_subscription_id', table_name='users')
    op.drop_index('ix_users_stripe_customer_id', table_name='users')
    
    # Drop columns
    op.drop_column('users', 'subscription_status')
    op.drop_column('users', 'stripe_subscription_id')
    op.drop_column('users', 'stripe_customer_id')
