from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User


def get_current_user(request: Request, db: Session) -> User | None:
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    return db.get(User, int(user_id))


def require_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    user = get_current_user(request, db)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Login required"
        )

    return user