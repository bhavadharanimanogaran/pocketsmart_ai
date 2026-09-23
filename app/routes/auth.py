from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import RegisterInput
from app.security import hash_password, verify_password, create_access_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    try:
        data = RegisterInput(name=name.strip(), email=email.strip().lower(), password=password)
    except Exception as exc:
        return templates.TemplateResponse("register.html", {"request": request, "error": str(exc)}, status_code=400)

    if db.query(User).filter(User.email == data.email).first():
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email already registered."}, status_code=400)

    user = User(name=data.name, email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    request.session["user_id"] = user.id
    request.session["user_name"] = user.name
    return RedirectResponse("/dashboard", status_code=303)

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email.strip().lower()).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid email or password."}, status_code=401)

    request.session["user_id"] = user.id
    request.session["user_name"] = user.name
    return RedirectResponse("/dashboard", status_code=303)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

@router.post("/token")
def token(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email.strip().lower()).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}
