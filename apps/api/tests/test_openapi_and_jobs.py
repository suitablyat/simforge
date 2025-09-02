from fastapi.testclient import TestClient
from app.main import app
from uuid import UUID

client = TestClient(app)

def test_openapi_exists():
    r = client.get("/openapi.json")
    assert r.status_code == 200
    spec = r.json()
    assert "/jobs" in spec["paths"]
    assert "/jobs/{job_id}" in spec["paths"]

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"ok": True}

def test_jobs_stub_flow():
    r = client.post("/jobs", json={"note":"quick sim"})
    assert r.status_code == 201
    job = r.json()
    UUID(job["id"])
    assert job["status"] == "queued"

    r2 = client.get(f"/jobs/{job['id']}")
    assert r2.status_code == 200
    job2 = r2.json()
    assert job2["id"] == job["id"]
