from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import ManagerCreate, UserResponse
from services.manager_service import create_manager_for_event

router = APIRouter(prefix="/api/managers", tags=["managers"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_manager(
    data: ManagerCreate,
    db: Session = Depends(get_db),
):
    return create_manager_for_event(db, data)
