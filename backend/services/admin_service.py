from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import User
from repositories import ban_repository, booking_repository, event_repository, user_repository
from repositories.user_repository import count_admins, delete_user, get_user_by_id, list_users


def get_all_users(db: Session, banned: bool | None = None) -> list[User]:
    users = list_users(db)
    banned_ids = ban_repository.get_banned_user_ids(db)
    for account in users:
        account.is_banned = account.id in banned_ids
    if banned is not None:
        return [account for account in users if account.is_banned is banned]
    return users


def get_admin_stats(db: Session) -> dict[str, int]:
    return {
        "total_bookings": booking_repository.count_bookings(db),
        "total_events": event_repository.count_events(db),
        "total_users": user_repository.count_users(db),
        "banned_users": ban_repository.count_banned_users(db),
    }


def get_all_bookings(db: Session) -> list[dict]:
    return booking_repository.list_all_bookings(db)


def ban_user_account(db: Session, user_id: int, current_admin_id: int) -> User:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.id == current_admin_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot ban your own account")
    if user.role != "user":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only regular user accounts can be banned")
    if ban_repository.is_user_banned(db, user.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already banned")

    ban_repository.add_ban(db, user.id)
    db.commit()
    db.refresh(user)
    user.is_banned = True
    return user


def unban_user_account(db: Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    ban = ban_repository.get_ban_by_user_id(db, user.id)
    if ban is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not banned")

    ban_repository.remove_ban(db, ban)
    db.commit()


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
