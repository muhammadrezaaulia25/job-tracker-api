import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


client = TestClient(app)


def make(company="Acme", position="Python Developer", **extra):
    return client.post("/applications", json={"company": company, "position": position, **extra})


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_get():
    res = make()
    assert res.status_code == 201
    body = res.json()
    assert body["status"] == "applied"
    assert client.get(f"/applications/{body['id']}").json()["company"] == "Acme"


def test_validation_error():
    assert client.post("/applications", json={"company": "", "position": "x"}).status_code == 422


def test_filter_and_stats():
    make("Acme")
    make("Globex", status="interview")
    assert len(client.get("/applications", params={"status": "interview"}).json()) == 1
    assert len(client.get("/applications", params={"company": "acm"}).json()) == 1
    stats = client.get("/applications/stats").json()
    assert stats["total"] == 2
    assert stats["by_status"]["interview"] == 1


def test_update_and_delete():
    app_id = make().json()["id"]
    res = client.patch(f"/applications/{app_id}", json={"status": "offer"})
    assert res.json()["status"] == "offer"
    assert client.delete(f"/applications/{app_id}").status_code == 204
    assert client.get(f"/applications/{app_id}").status_code == 404
