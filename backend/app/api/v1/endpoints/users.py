"""
User profile endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user = Depends(get_current_user)
):
    """
    Get current user profile
    """
    # TODO: Return user profile
    pass


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update user profile
    """
    # TODO: Implement profile update
    pass


@router.delete("/me", status_code=204)
async def delete_user_account(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete user account (soft delete)
    """
    # TODO: Implement account deletion
    pass
