from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import BookingCreate, BookingResponse
from services import booking_service

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def book_event(
    data: BookingCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    return booking_service.create_booking(db, request.state.current_user, data)


@router.get("/my", response_model=list[BookingResponse])
def my_bookings(
    request: Request,
    db: Session = Depends(get_db),
):
    return booking_service.get_my_bookings(db, request.state.current_user)


@router.get("/event/{event_id}", response_model=list[BookingResponse])
def event_bookings(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    return booking_service.get_event_bookings(db, event_id, request.state.current_user)


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(
    booking_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    booking_service.cancel_booking(db, booking_id, request.state.current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
