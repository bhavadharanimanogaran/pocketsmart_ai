from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import FileResponse


from app.config import settings
from app.database import init_db
from app.routes.auth import router as auth_router
from app.routes.dashboard import router as dashboard_router
from app.planners import router as planner_router
from app.routes.api import router as api_router


BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="PocketSmart AI - Smart Budget and Recommendation Assistant",
    lifespan=lifespan,
)


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET,
    same_site="lax",
    https_only=False,
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


app.include_router(auth_router)
app.include_router(planner_router)
app.include_router(dashboard_router)
app.include_router(api_router)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "ai_model": settings.GEMINI_MODEL,
    }
@app.get("/homeplanner.html")
def homeplanner(request: Request):
    return templates.TemplateResponse(
        "homeplanner.html",
        {"request": request}
    )


@app.get("/jewellery.html")
def jewellery(request: Request):
    return templates.TemplateResponse(
        "jewellery.html",
        {"request": request}
    )


@app.get("/partyplanner.html")
def partyplanner(request: Request):
    return templates.TemplateResponse(
        "planner.html",
        {"request": request}
    )