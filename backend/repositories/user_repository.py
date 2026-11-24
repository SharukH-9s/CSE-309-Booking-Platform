from sqlalchemy.orm import Session

from models import User


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower()).first()


def add_user(db: Session, user: User) -> User:
    db.add(user)
    db.flush()
    return user
