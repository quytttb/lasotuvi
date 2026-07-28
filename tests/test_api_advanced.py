"""Advanced API endpoint tests (English schema v2)."""
import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

BIRTH = {
    "day": 15,
    "month": 8,
    "year": 1990,
    "hour": 7,
    "gender": 1,
    "is_solar": True,
    "timezone": 7,
}


class TestChartAnalysisEndpoints:
    def test_chart_analyze_success(self):
        response = client.post("/chart/analyze", json=BIRTH)
        assert response.status_code == 200
        data = response.json()
        assert "life_palace_analysis" in data
        assert "overall_strength" in data
        assert "major_life_events" in data

    def test_chart_analyze_with_name(self):
        payload = {**BIRTH, "name": "Nguyen Van A", "view_year": 2026}
        response = client.post("/chart/analyze", json=payload)
        assert response.status_code == 200
        assert response.json()["birth_info"]["name"] == "Nguyen Van A"


class TestBatchEndpoints:
    def test_batch_success(self):
        response = client.post(
            "/chart/batch",
            json={"charts": [BIRTH, {**BIRTH, "gender": -1, "name": "B"}]},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert data["successful"] == 2


class TestInfoEndpoints:
    def test_stars(self):
        response = client.get("/info/stars")
        assert response.status_code == 200
        assert response.json()["total"] >= 100

    def test_elements(self):
        response = client.get("/info/elements")
        assert response.status_code == 200
        assert len(response.json()["elements"]) == 5

    def test_stem_branch_info(self):
        response = client.get("/info/stem-branch")
        assert response.status_code == 200
        data = response.json()
        assert data["heavenly_stems"]["count"] == 10
        assert data["earthly_branches"]["count"] == 12

    def test_stats(self):
        response = client.get("/stats")
        assert response.status_code == 200
        assert response.json()["schema"] == "english_v2_breaking"
