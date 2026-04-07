from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from ai_schools.app import create_app


def test_health() -> None:
    app = create_app()
    client = TestClient(app)
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_index_html_renders() -> None:
    app = create_app()
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert "AI Schools" in r.text


def test_list_districts_and_get_score() -> None:
    app = create_app()
    client = TestClient(app)

    r = client.get("/api/districts", params={"limit": 2})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2
    district_id = items[0]["id"]

    r2 = client.get(f"/api/districts/{district_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == district_id

    r3 = client.get(f"/api/districts/{district_id}/score")
    assert r3.status_code == 200
    assert 0 <= r3.json()["score"] <= 100


def test_list_districts_rejects_bad_limit() -> None:
    app = create_app()
    client = TestClient(app)
    r = client.get("/api/districts", params={"limit": 0})
    assert r.status_code == 400


def test_get_district_404() -> None:
    app = create_app()
    client = TestClient(app)
    r = client.get("/api/districts/does-not-exist")
    assert r.status_code == 404


def test_score_district_404() -> None:
    app = create_app()
    client = TestClient(app)
    r = client.get("/api/districts/does-not-exist/score")
    assert r.status_code == 404


def test_top_endpoint() -> None:
    app = create_app()
    client = TestClient(app)
    r = client.post("/api/top", json={"n": 3, "state": "CA"})
    assert r.status_code == 200
    scored = r.json()
    assert len(scored) <= 3
    if scored:
        assert "district" in scored[0]
        assert "score" in scored[0]


def test_top_endpoint_with_custom_weights() -> None:
    app = create_app()
    client = TestClient(app)
    r = client.post(
        "/api/top",
        json={
            "n": 2,
            "weights": {
                "graduation_rate": 1,
                "math_proficiency": 1,
                "reading_proficiency": 1,
                "student_teacher_ratio": 1,
                "per_pupil_spending": 1,
            },
        },
    )
    assert r.status_code == 200
    scored = r.json()
    assert len(scored) == 2


def test_default_data_file_exists_in_repo() -> None:
    # Guards the "runnable out of the box" requirement.
    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "districts_sample.csv").exists()

