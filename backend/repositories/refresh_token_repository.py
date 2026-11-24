from datetime import datetime

from sqlalchemy.orm import Session

from models import RefreshToken


def get_by_hash_for_update(db: Session, token_hash: str) -> RefreshToken | None:
    return (
        db.query(RefreshToken)
        .filter(RefreshToken.token_hash == token_hash)
        .with_for_update()
        .first()
    )


def add_refresh_token(db: Session, record: RefreshToken) -> RefreshToken:
    db.add(record)
    db.flush()
    return record


def revoke_user_tokens(db: Session, user_id: int, revoked_at: datetime) -> None:
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked_at.is_(None),
    ).update({RefreshToken.revoked_at: revoked_at}, synchronize_session=False)
