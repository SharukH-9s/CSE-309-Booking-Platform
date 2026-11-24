from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import AdminStatsResponse, BookingResponse, UserResponse
from services.admin_service import (
    ban_user_account,
    delete_user_account,
    get_admin_stats,
    get_all_bookings,
    get_all_users,
    unban_user_account,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStatsResponse)
def read_admin_stats(db: Session = Depends(get_db)):
    return get_admin_stats(db)


@router.get("/bookings", response_model=list[BookingResponse])
def list_platform_bookings(db: Session = Depends(get_db)):
    return get_all_bookings(db)


@router.get("/users", response_model=list[UserResponse])
def list_all_users(banned: bool | None = None, db: Session = Depends(get_db)):
    return get_all_users(db, banned=banned)


@router.post("/users/{user_id}/ban", response_model=UserResponse)
def ban_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    return ban_user_account(db, user_id, request.state.current_user.id)


@router.delete("/users/{user_id}/ban", status_code=status.HTTP_204_NO_CONTENT)
def unban_user(user_id: int, db: Session = Depends(get_db)):
    unban_user_account(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    delete_user_account(db, user_id, request.state.current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
