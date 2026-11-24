from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Booking, Event, User


def add_booking(db: Session, booking: Booking) -> Booking:
    db.add(booking)
    db.flush()
    return booking


def get_booking_by_id(db: Session, booking_id: int) -> Booking | None:
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_user_booking_for_event(db: Session, user_id: int, event_id: int) -> Booking | None:
    return db.query(Booking).filter(Booking.user_id == user_id, Booking.event_id == event_id).first()


def delete_booking(db: Session, booking: Booking) -> None:
    db.delete(booking)


def count_bookings(db: Session) -> int:
    return db.query(func.count(Booking.id)).scalar() or 0


def list_bookings_by_user(db: Session, user_id: int) -> list[dict]:
    results = (
        db.query(Booking, Event)
        .join(Event, Booking.event_id == Event.id)
        .filter(Booking.user_id == user_id)
        .order_by(Booking.created_at.desc())
        .all()
    )
    return [
        {
            "id": b.id,
            "event_id": b.event_id,
            "user_id": b.user_id,
            "created_at": b.created_at,
            "event_title": e.title,
            "event_date": e.event_date,
            "event_location": e.location,
        }
        for b, e in results
    ]


def list_bookings_by_event(db: Session, event_id: int) -> list[dict]:
    results = (
        db.query(Booking, User, Event)
        .join(User, Booking.user_id == User.id)
        .join(Event, Booking.event_id == Event.id)
        .filter(Booking.event_id == event_id)
        .order_by(Booking.created_at.desc())
        .all()
    )
    return [
        {
            "id": b.id,
            "event_id": b.event_id,
            "user_id": b.user_id,
            "created_at": b.created_at,
            "user_name": u.name,
            "user_email": u.email,
            "event_title": e.title,
            "event_date": e.event_date,
            "event_location": e.location,
        }
        for b, u, e in results
    ]


def list_all_bookings(db: Session) -> list[dict]:
    results = (
        db.query(Booking, User, Event)
        .join(User, Booking.user_id == User.id)
        .join(Event, Booking.event_id == Event.id)
        .order_by(Booking.created_at.desc())
        .all()
    )
    return [
        {
            "id": b.id,
            "event_id": b.event_id,
            "user_id": b.user_id,
            "created_at": b.created_at,
            "user_name": u.name,
            "user_email": u.email,
            "event_title": e.title,
            "event_date": e.event_date,
            "event_location": e.location,
        }
        for b, u, e in results
    ]
