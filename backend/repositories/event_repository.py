from sqlalchemy.orm import Session

from models import Event


def list_events(db: Session) -> list[Event]:
    return db.query(Event).order_by(Event.event_date, Event.id).all()


def list_manager_events(db: Session, manager_id: int) -> list[Event]:
    return db.query(Event).filter(Event.manager_id == manager_id).order_by(Event.event_date, Event.id).all()


def get_event(db: Session, event_id: int) -> Event | None:
    return db.query(Event).filter(Event.id == event_id).first()


def add_event(db: Session, event: Event) -> Event:
    db.add(event)
    db.flush()
    return event


def delete_event(db: Session, event: Event) -> None:
    db.delete(event)
