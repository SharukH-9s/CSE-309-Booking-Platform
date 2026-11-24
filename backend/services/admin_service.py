from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import User
from repositories import event_repository
from repositories.user_repository import count_admins, delete_user, get_user_by_id, list_users


def get_all_users(db: Session) -> list[User]:
    return list_users(db)


def delete_user_account(db: Session, user_id: int, current_admin_id: int) -> None:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.id == current_admin_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot delete your own account")
    if user.role == "admin" and count_admins(db) <= 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete the last admin")

    event_repository.unassign_manager(db, user.id)
    delete_user(db, user)
    db.commit()
