import os
os.environ["DATABASE_URL"] = "sqlite:///./test_pocketsmart.db"
os.environ["AI_ENABLED"] = "false"

from fastapi.testclient import TestClient
from app import app
from app.database import init_db

init_db()
client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_register_and_login():
    email = "test@example.com"
    r = client.post("/register", data={"name": "Test User", "email": email, "password": "secret123"}, follow_redirects=False)
    assert r.status_code == 303
    assert r.headers["location"] == "/dashboard"

    client.get("/logout")
    r = client.post("/login", data={"email": email, "password": "secret123"}, follow_redirects=False)
    assert r.status_code == 303
    assert r.headers["location"] == "/dashboard"

def test_home_planner_requires_login():
    client.get("/logout")
    r = client.post("/generate-home", data={"budget":10000,"rooms":"Living room","style":"minimal","needs":"lights"}, follow_redirects=False)
    assert r.status_code == 401

def test_home_planner_after_login():
    client.post("/login", data={"email":"test@example.com","password":"secret123"}, follow_redirects=False)
    r = client.post("/generate-home", data={"budget":30000,"rooms":"Living room, bedroom","style":"minimal","needs":"lights and storage"}, follow_redirects=False)
    assert r.status_code == 303
    assert r.headers["location"].startswith("/recommendations-details/")
