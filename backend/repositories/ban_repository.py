from sqlalchemy.orm import Session

from models import BannedUser


def is_user_banned(db: Session, user_id: int) -> bool:
    return db.query(BannedUser.id).filter(BannedUser.user_id == user_id).first() is not None


def get_banned_user_ids(db: Session) -> set[int]:
    rows = db.query(BannedUser.user_id).all()
    return {user_id for (user_id,) in rows}


def get_ban_by_user_id(db: Session, user_id: int) -> BannedUser | None:
    return db.query(BannedUser).filter(BannedUser.user_id == user_id).first()


def add_ban(db: Session, user_id: int) -> BannedUser:
    ban = BannedUser(user_id=user_id)
    db.add(ban)
    db.flush()
    return ban


def remove_ban(db: Session, ban: BannedUser) -> None:
    db.delete(ban)
