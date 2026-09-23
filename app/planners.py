import json
from pathlib import Path

from fastapi import APIRouter, Request, UploadFile, File, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies import require_user, get_current_user
from app.models import RecommendationHistory
from app.services.planner_service import (
    generate_home,
    generate_party,
    generate_jewelry,
)


router = APIRouter()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_history(db, user, planner_type, budget, request_data, result):
    item = RecommendationHistory(
        user_id=user.id,
        planner_type=planner_type,
        budget=budget,
        request_json=json.dumps(request_data),
        response_json=json.dumps(result),
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


# ---------------- HOME PLANNER ----------------

@router.get("/home-planner", response_class=HTMLResponse)
def home_page(
    request: Request,
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        "homeplanner.html",
        {
            "request": request,
            "user": user
        }
    )


# ---------------- PARTY PLANNER ----------------

@router.get("/party-planner", response_class=HTMLResponse)
def party_page(
    request: Request,
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        "partyplanner.html",
        {
            "request": request,
            "user": user
        }
    )


# ---------------- JEWELLERY PLANNER ----------------

@router.get("/jewelry-planner", response_class=HTMLResponse)
def jewelry_page(
    request: Request,
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        "jewellery.html",
        {
            "request": request,
            "user": user
        }
    )


# ---------------- GENERATE HOME ----------------

@router.post("/generate-home")
def home_generate(
    request: Request,
    budget: int = Form(...),
    rooms: str = Form(...),
    style: str = Form(...),
    needs: str = Form(...),
    db: Session = Depends(get_db),
):
    user = require_user(request, db)

    result = generate_home(
        budget,
        rooms,
        style,
        needs
    )

    item = save_history(
        db,
        user,
        "home",
        budget,
        {
            "budget": budget,
            "rooms": rooms,
            "style": style,
            "needs": needs
        },
        result
    )

    return RedirectResponse(
        f"/recommendations-details/{item.id}",
        status_code=303
    )


# ---------------- GENERATE PARTY ----------------

@router.post("/generate-party")
def party_generate(
    request: Request,
    budget: int = Form(...),
    guests: int = Form(...),
    event_type: str = Form(...),
    venue: str = Form(...),
    preferences: str = Form(""),
    db: Session = Depends(get_db),
):
    user = require_user(request, db)

    result = generate_party(
        budget,
        guests,
        event_type,
        venue,
        preferences
    )

    item = save_history(
        db,
        user,
        "party",
        budget,
        {
            "budget": budget,
            "guests": guests,
            "event_type": event_type,
            "venue": venue,
            "preferences": preferences
        },
        result
    )

    return RedirectResponse(
        f"/recommendations-details/{item.id}",
        status_code=303
    )


# ---------------- GENERATE JEWELLERY ----------------

@router.post("/generate-jewelry")
async def jewelry_generate(
    request: Request,
    budget: int = Form(...),
    occasion: str = Form(...),
    style: str = Form(...),
    outfit_description: str = Form(""),
    outfit_image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    user = require_user(request, db)

    image_bytes = None
    image_type = None

    if outfit_image and outfit_image.filename:

        if outfit_image.content_type not in settings.allowed_image_types:
            return templates.TemplateResponse(
                "jewellery.html",
                {
                    "request": request,
                    "user": user,
                    "error": "Upload JPG, PNG or WebP only."
                },
                status_code=400
            )

        image_bytes = await outfit_image.read()

        if len(image_bytes) > settings.MAX_UPLOAD_MB * 1024 * 1024:
            return templates.TemplateResponse(
                "jewellery.html",
                {
                    "request": request,
                    "user": user,
                    "error": f"Image must be under {settings.MAX_UPLOAD_MB} MB."
                },
                status_code=400
            )

        image_type = outfit_image.content_type

    result = generate_jewelry(
        budget,
        occasion,
        style,
        outfit_description,
        image_bytes,
        image_type
    )

    item = save_history(
        db,
        user,
        "jewelry",
        budget,
        {
            "budget": budget,
            "occasion": occasion,
            "style": style,
            "outfit_description": outfit_description,
            "image_uploaded": bool(image_bytes)
        },
        result
    )

    return RedirectResponse(
        f"/recommendations-details/{item.id}",
        status_code=303
    )