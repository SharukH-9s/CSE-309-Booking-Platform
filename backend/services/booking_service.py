from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Booking, User
from repositories import ban_repository, booking_repository, event_repository
from schemas import BookingCreate


def create_booking(db: Session, user: User, data: BookingCreate) -> dict:
    if ban_repository.is_user_banned(db, user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is banned from booking events",
        )

    event = event_repository.get_event(db, data.event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    existing = booking_repository.get_user_booking_for_event(db, user.id, data.event_id)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already booked this event",
        )

    booking = Booking(event_id=data.event_id, user_id=user.id)
    booking_repository.add_booking(db, booking)
    db.commit()
    db.refresh(booking)

    return {
        "id": booking.id,
        "event_id": booking.event_id,
        "user_id": booking.user_id,
        "created_at": booking.created_at,
        "user_name": user.name,
        "user_email": user.email,
        "event_title": event.title,
        "event_date": event.event_date,
        "event_location": event.location,
    }


def get_my_bookings(db: Session, user: User) -> list[dict]:
    return booking_repository.list_bookings_by_user(db, user.id)


def get_event_bookings(db: Session, event_id: int, current_user: User) -> list[dict]:
    event = event_repository.get_event(db, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    if current_user.role == "manager" and event.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not manage this event",
        )

    return booking_repository.list_bookings_by_event(db, event_id)


def cancel_booking(db: Session, booking_id: int, current_user: User) -> None:
    booking = booking_repository.get_booking_by_id(db, booking_id)
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    event = event_repository.get_event(db, booking.event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    if current_user.role == "manager" and event.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel bookings for your assigned event",
        )
    elif current_user.role == "user" and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot cancel another user's booking",
        )

    booking_repository.delete_booking(db, booking)
    db.commit()
