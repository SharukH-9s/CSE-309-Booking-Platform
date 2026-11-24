from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import RefreshToken, User
from repositories import refresh_token_repository
from repositories.user_repository import add_user, get_user_by_email, get_user_by_id
from schemas import PasswordChange, TokenResponse, UserProfileUpdate, UserRegister, UserResponse
from security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    refresh_token_expiration,
    verify_password,
)


def register_user(db: Session, data: UserRegister) -> User:
    email = data.email.lower()
    if get_user_by_email(db, email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")
    user = User(
        name=data.name.strip(),
        email=email,
        phone=data.phone,
        hashed_password=hash_password(data.password),
        role="user",
    )
    add_user(db, user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email.strip().lower())
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return user


def create_token_pair(db: Session, user: User) -> TokenResponse:
    refresh_token = create_refresh_token()
    refresh_token_repository.add_refresh_token(
        db,
        RefreshToken(
            user_id=user.id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=refresh_token_expiration(),
        ),
    )
    db.commit()
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


def rotate_refresh_token(db: Session, raw_token: str) -> TokenResponse:
    now = datetime.now(timezone.utc)
    current = refresh_token_repository.get_by_hash_for_update(db, hash_refresh_token(raw_token))
    if current is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    if current.revoked_at is not None:
        # Reuse of an old token can mean a stolen token was replayed; invalidate this user's sessions.
        refresh_token_repository.revoke_user_tokens(db, current.user_id, now)
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has already been used")

    if current.expires_at <= now:
        current.revoked_at = now
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired")

    user = get_user_by_id(db, current.user_id)
    if user is None:
        current.revoked_at = now
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    current.revoked_at = now
    next_token = create_refresh_token()
    refresh_token_repository.add_refresh_token(
        db,
        RefreshToken(
            user_id=user.id,
            token_hash=hash_refresh_token(next_token),
            expires_at=refresh_token_expiration(),
        ),
    )
    db.commit()
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=next_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


def revoke_refresh_token(db: Session, raw_token: str) -> None:
    record = refresh_token_repository.get_by_hash_for_update(db, hash_refresh_token(raw_token))
    if record is not None and record.revoked_at is None:
        record.revoked_at = datetime.now(timezone.utc)
        db.commit()


def update_user_profile(db: Session, user_id: int, data: UserProfileUpdate) -> User:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    changes = data.model_dump(exclude_unset=True)
    if "name" in changes:
        name = changes["name"].strip()
        if not name:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Name cannot be empty")
        user.name = name
    if "email" in changes:
        email = changes["email"].strip().lower()
        existing_user = get_user_by_email(db, email)
        if existing_user is not None and existing_user.id != user.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")
        user.email = email
    if "phone" in changes:
        user.phone = changes["phone"].strip() if changes["phone"] else None

    db.commit()
    db.refresh(user)
    return user


def change_user_password(db: Session, user_id: int, data: PasswordChange) -> None:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(data.current_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    if data.current_password == data.new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be different")

    user.hashed_password = hash_password(data.new_password)
    refresh_token_repository.revoke_user_tokens(db, user.id, datetime.now(timezone.utc))
    db.commit()


def seed_admin(db: Session) -> None:
    import os

    email = os.getenv("ADMIN_EMAIL", "").strip().lower()
    name = os.getenv("ADMIN_NAME", "").strip()
    phone = os.getenv("ADMIN_PHONE", "").strip()
    password = os.getenv("ADMIN_PASSWORD", "")
    configured = [bool(email), bool(name), bool(phone), bool(password)]
    if not any(configured):
        return
    if not all(configured):
        raise RuntimeError("Set ADMIN_EMAIL, ADMIN_NAME, ADMIN_PHONE, and ADMIN_PASSWORD together")
    existing_admin_email = get_user_by_email(db, email)
    if existing_admin_email:
        if existing_admin_email.role != "admin":
            raise RuntimeError("ADMIN_EMAIL belongs to a non-admin account; choose an unused email")
        return
    add_user(
        db,
        User(
            name=name,
            email=email,
            phone=phone,
            hashed_password=hash_password(password),
            role="admin",
        ),
    )
    db.commit()


def get_profile(db: Session, user_id: int) -> User | None:
    return get_user_by_id(db, user_id)
