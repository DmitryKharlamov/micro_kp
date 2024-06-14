# security_service/tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from ..main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

def test_register_user(client):
    response = client.post("/register", json={"username": "testuser", "password": "testpassword", "role": "jack"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login_user(client):
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_user_me(client):
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    token = response.json()["access_token"]
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
