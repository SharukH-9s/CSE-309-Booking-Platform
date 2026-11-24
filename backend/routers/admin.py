from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserResponse
from services.admin_service import delete_user_account, get_all_users

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=list[UserResponse])
def list_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    delete_user_account(db, user_id, request.state.current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
