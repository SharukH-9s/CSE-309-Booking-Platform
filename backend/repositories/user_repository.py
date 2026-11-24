from sqlalchemy import func
from sqlalchemy.orm import Session

from models import User


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower()).first()


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.role, User.name, User.id).all()


def count_users(db: Session) -> int:
    return db.query(func.count(User.id)).scalar() or 0


def count_admins(db: Session) -> int:
    return db.query(func.count(User.id)).filter(User.role == "admin").scalar() or 0


def add_user(db: Session, user: User) -> User:
    db.add(user)
    db.flush()
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
