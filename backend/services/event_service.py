from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Event, User
from repositories import event_repository
from schemas import EventCreate, EventUpdate


def _get_event_or_404(db: Session, event_id: int) -> Event:
    event = event_repository.get_event(db, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


def list_events(db: Session, current_user: User | None) -> list[Event]:
    if current_user is not None and current_user.role == "manager":
        return event_repository.list_manager_events(db, current_user.id)
    return event_repository.list_events(db)


def get_event(db: Session, event_id: int, current_user: User | None) -> Event:
    event = _get_event_or_404(db, event_id)
    _check_manager_ownership(event, current_user)
    return event


def create_event(db: Session, data: EventCreate) -> Event:
    event = Event(**data.model_dump())
    event_repository.add_event(db, event)
    db.commit()
    db.refresh(event)
    return event


def update_event(db: Session, event_id: int, data: EventUpdate, current_user: User) -> Event:
    event = _get_event_or_404(db, event_id)
    _check_manager_ownership(event, current_user)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    return event


def delete_event(db: Session, event_id: int, current_user: User) -> None:
    event = _get_event_or_404(db, event_id)
    _check_manager_ownership(event, current_user)
    event_repository.delete_event(db, event)
    db.commit()


def _check_manager_ownership(event: Event, current_user: User | None) -> None:
    if current_user is not None and current_user.role == "manager" and event.manager_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This event is not assigned to you")
