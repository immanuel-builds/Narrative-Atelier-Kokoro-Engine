import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.auth.auth import get_password_hash

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_setup():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_landing():
    response = client.get("/")
    assert response.status_code == 200
    assert "Kokoro Engine" in response.text
    assert "Built to sharpen authors" in response.text

def test_registration():
    response = client.post(
        "/auth/register",
        data={"username": "testwriter", "email": "test@example.com", "password": "password123"},
        follow_redirects=False
    )
    assert response.status_code == 302
    assert response.headers["location"] == "/auth/login"

def test_login():
    response = client.post(
        "/auth/login",
        data={"email": "test@example.com", "password": "password123"},
        follow_redirects=False
    )
    assert response.status_code == 302
    assert response.headers["location"] == "/dashboard"
    assert "session" in response.cookies

def test_project_creation():
    # Login first
    login_res = client.post(
        "/auth/login",
        data={"email": "test@example.com", "password": "password123"},
        follow_redirects=True
    )
    session_cookie = login_res.cookies.get("session")

    # Create project
    response = client.post(
        "/projects/create",
        data={"title": "My Great Novel", "description": "An epic journey."},
        cookies={"session": session_cookie},
        follow_redirects=False
    )
    assert response.status_code == 302
    assert response.headers["location"] == "/dashboard"

def test_chapter_creation():
    # Login
    login_res = client.post(
        "/auth/login",
        data={"email": "test@example.com", "password": "password123"},
        follow_redirects=True
    )
    session_cookie = login_res.cookies.get("session")

    # Get dashboard to find project id (or just use 1 if it's the first)
    response = client.post(
        "/editor/1/chapters/create",
        data={"title": "Chapter One"},
        cookies={"session": session_cookie},
        follow_redirects=False
    )
    assert response.status_code == 302
    assert "/editor/1?chapter_id=" in response.headers["location"]

if __name__ == "__main__":
    # Simple manual run
    test_setup()
    test_landing()
    test_registration()
    test_login()
    test_project_creation()
    test_chapter_creation()
    print("All functional tests passed!")
