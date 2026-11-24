from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    LoginRequest,
    PasswordChange,
    RefreshRequest,
    TokenResponse,
    UserProfileUpdate,
    UserRegister,
    UserResponse,
)
from services.auth_service import (
    authenticate_user,
    change_user_password,
    create_token_pair,
    register_user,
    revoke_refresh_token,
    rotate_refresh_token,
    update_user_profile,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, data)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    return create_token_pair(db, user)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    return rotate_refresh_token(db, data.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(data: RefreshRequest, db: Session = Depends(get_db)):
    revoke_refresh_token(db, data.refresh_token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
