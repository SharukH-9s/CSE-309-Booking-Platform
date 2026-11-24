from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import BookingResponse, EventCreate, EventResponse, EventUpdate
from services import booking_service, event_service

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("", response_model=list[EventResponse])
def list_events(
    request: Request,
    db: Session = Depends(get_db),
):
    return event_service.list_events(db, request.state.current_user)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    return event_service.get_event(db, event_id, request.state.current_user)


@router.get("/{event_id}/bookings", response_model=list[BookingResponse])
def get_event_bookings(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    return booking_service.get_event_bookings(db, event_id, request.state.current_user)


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    data: EventCreate,
    db: Session = Depends(get_db),
):
    return event_service.create_event(db, data)


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    data: EventUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    return event_service.update_event(db, event_id, data, request.state.current_user)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    event_service.delete_event(db, event_id, request.state.current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
