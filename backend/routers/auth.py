from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import LoginRequest, PasswordChange, TokenResponse, UserProfileUpdate, UserRegister, UserResponse
from security import create_access_token
from services.auth_service import (
    authenticate_user,
    change_user_password,
    register_user,
    update_user_profile,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, data)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    profile = UserResponse.model_validate(user)
    return TokenResponse(
        access_token=create_access_token(profile.id),
        user=profile,
    )


@router.get("/me", response_model=UserResponse)
def me(request: Request):
    return request.state.current_user


@router.patch("/me", response_model=UserResponse)
def update_me(data: UserProfileUpdate, request: Request, db: Session = Depends(get_db)):
    return update_user_profile(db, request.state.current_user.id, data)


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(data: PasswordChange, request: Request, db: Session = Depends(get_db)):
    change_user_password(db, request.state.current_user.id, data)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
