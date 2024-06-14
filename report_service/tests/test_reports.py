# report_service/tests/test_reports.py
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

def test_create_report(client):
    response = client.post("/report", json={"role": "jack"})
    assert response.status_code == 200
    assert response.json()["role"] == "jack"
    assert "content" in response.json()

def test_read_report(client):
    response = client.post("/report", json={"role": "jack"})
    report_id = response.json()["id"]
    response = client.get(f"/reports/{report_id}")
    assert response.status_code == 200
    assert response.json()["id"] == report_id
    assert response.json()["role"] == "jack"
