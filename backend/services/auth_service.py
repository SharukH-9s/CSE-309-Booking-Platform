from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import User
from repositories.user_repository import add_user, get_user_by_email, get_user_by_id
from schemas import PasswordChange, UserProfileUpdate, UserRegister
from security import hash_password, verify_password


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
