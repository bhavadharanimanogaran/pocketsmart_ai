# PocketSmart AI

A complete FastAPI + Jinja2 + SQLite + Google Gemini application based on the supplied PocketSmart AI project documentation.

## Features

- User registration, login, logout and JWT token endpoint
- Session-aware dashboard
- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner with optional outfit image upload
- Gemini multimodal integration for jewelry images
- Structured JSON AI output validated with Pydantic
- Deterministic fallback recommendations when Gemini is unavailable
- Recommendation history
- Mock provider catalog for Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO-style links
- Responsive HTML/CSS/JavaScript frontend
- Automated API tests

## Important implementation note

The supplied document names Gemini 1.5 Flash Pro and also mixes Flask and FastAPI terminology. This implementation standardizes the backend on **FastAPI**, matching the later milestones and route definitions in the document.

The Gemini model is configurable through `GEMINI_MODEL`. It defaults to `gemini-2.5-flash` because model availability changes over time. You can change it without editing application code.

The document asks for Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO sourcing but does not provide API credentials or official partner API contracts. Therefore this project uses a provider abstraction with safe search links and a local mock catalog. It does **not** pretend that scraped/live prices are real.

## 1. VS Code setup

Install:

- Python 3.11+
- VS Code
- Git (optional)

Open this project folder in VS Code.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## 2. Gemini API key

Create a Gemini API key in Google AI Studio / Google AI for Developers, then put it in `.env`:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
AI_ENABLED=true
```

You can run the application without a key. In that mode the deterministic fallback engine is used, so the UI and all routes remain testable.

## 3. Run

```bash
uvicorn app:app --reload
```

Open:

http://127.0.0.1:8000

## 4. Test

```bash
pytest -q
```

Health check:

http://127.0.0.1:8000/health

## 5. Project structure

```text
PocketSmartAI/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── planners.py
│   │   ├── dashboard.py
│   │   └── api.py
│   └── services/
│       ├── __init__.py
│       ├── ai_service.py
│       ├── planner_service.py
│       └── providers.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── history.html
│   ├── home_planner.html
│   ├── party_planner.html
│   ├── jewelry_planner.html
│   └── recommendations.html
├── static/
│   ├── css/style.css
│   └── js/app.js
├── uploads/.gitkeep
└── tests/test_app.py
```

## 6. Test accounts

The application has no pre-created account. Register from `/register`.

## 7. API routes

- `GET /health`
- `GET /register`
- `POST /register`
- `GET /login`
- `POST /login`
- `GET /logout`
- `POST /token`
- `GET /session-info`
- `GET /session-data`
- `POST /generate-home`
- `POST /generate-party`
- `POST /generate-jewelry`
- `GET /recommendations-details/{history_id}`
- `GET /history`
- `GET /startup`

All planner endpoints require a logged-in session.

## 8. Production notes

Before deployment:

- Use PostgreSQL instead of SQLite.
- Set strong random secrets.
- Enable HTTPS and secure cookies.
- Add CSRF protection for form POSTs.
- Replace mock provider adapters with authorized partner APIs.
- Add rate limiting and request logging.
- Store uploaded images outside the application container.
- Never commit `.env` or API keys.
