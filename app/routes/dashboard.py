import json
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import RecommendationHistory, User
from app.dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    history = (
        db.query(RecommendationHistory)
        .filter_by(user_id=user.id)
        .order_by(RecommendationHistory.created_at.desc())
        .limit(5)
        .all()
    )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "history": history
        }
    )


@router.get("/history", response_class=HTMLResponse)
def history(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    items = (
        db.query(RecommendationHistory)
        .filter_by(user_id=user.id)
        .order_by(RecommendationHistory.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "user": user,
            "items": items
        }
    )


@router.get("/recommendations-details/{history_id}", response_class=HTMLResponse)
def details(history_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    item = (
        db.query(RecommendationHistory)
        .filter_by(id=history_id, user_id=user.id)
        .first()
    )

    if not item:
        return RedirectResponse("/history", status_code=303)

    result = json.loads(item.response_json)

    return templates.TemplateResponse(
        "recommendation.html",
        {
            "request": request,
            "user": user,
            "result": result,
            "history": item
        }
    )


@router.get("/session-info")
def session_info(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)

    return {
        "logged_in": bool(user),
        "user_id": user.id if user else None,
        "name": user.name if user else None
    }


@router.get("/session-data")
def session_data(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)

    if not user:
        return {
            "logged_in": False,
            "history_count": 0
        }

    count = (
        db.query(RecommendationHistory)
        .filter_by(user_id=user.id)
        .count()
    )

    return {
        "logged_in": True,
        "user_id": user.id,
        "history_count": count
    }


@router.get("/startup")
def startup():
    return {"status": "ready"}