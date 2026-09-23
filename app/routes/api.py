from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_user
from app.services.planner_service import generate_home, generate_party


router = APIRouter(prefix="/api")


# =========================
# HOME PLANNER API
# =========================

@router.post("/home")
def api_home(
    payload: dict,
    request: Request,
    db: Session = Depends(get_db)
):
    require_user(request, db)

    return generate_home(
        int(payload["budget"]),
        payload["rooms"],
        payload["style"],
        payload["needs"]
    )


# =========================
# PARTY PLANNER API
# =========================

@router.post("/party")
def api_party(
    payload: dict,
    request: Request,
    db: Session = Depends(get_db)
):
    require_user(request, db)

    return generate_party(
        int(payload["budget"]),
        int(payload["guests"]),
        payload["event_type"],
        payload["venue"],
        payload.get("preferences", "")
    )