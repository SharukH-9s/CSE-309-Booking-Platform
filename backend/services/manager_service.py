from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import User
from repositories import event_repository
from repositories.user_repository import add_user, get_user_by_email
from schemas import ManagerCreate
from security import hash_password


def create_manager_for_event(db: Session, data: ManagerCreate) -> User:
    event = event_repository.get_event(db, data.event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if event.manager_id is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Event already has a manager")
    if get_user_by_email(db, data.email.lower()):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

    manager = User(
        name=data.name.strip(),
        email=data.email.lower(),
        phone=data.phone,
        hashed_password=hash_password(data.password),
        role="manager",
    )
    try:
        add_user(db, manager)
        event.manager_id = manager.id
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(manager)
    return manager
