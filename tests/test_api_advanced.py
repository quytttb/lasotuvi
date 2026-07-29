"""Advanced API endpoint tests (English schema v2)."""

from fastapi.testclient import TestClient

from api.main import app
from api.services import TuViService
from lasotuvi.iztro_adapter import IztroTimeoutError

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

    def test_batch_does_not_expose_internal_errors(self, monkeypatch):
        def fail(_birth):
            raise RuntimeError("private implementation detail")

        monkeypatch.setattr(TuViService, "generate_full_chart", fail)
        response = client.post("/chart/batch", json={"charts": [BIRTH]})
        assert response.status_code == 200
        assert response.json()["results"][0]["detail"] is None


class TestProductionSafety:
    def test_internal_error_response_is_generic(self, monkeypatch):
        def fail(_birth):
            raise RuntimeError("private implementation detail")

        monkeypatch.setattr(TuViService, "generate_full_chart", fail)
        safe_client = TestClient(app, raise_server_exceptions=False)
        response = safe_client.post("/chart/generate", json=BIRTH)
        assert response.status_code == 500
        assert "private implementation detail" not in response.text
        assert response.json()["request_id"]

    def test_engine_timeout_returns_service_unavailable(self, monkeypatch):
        def fail(_birth):
            raise IztroTimeoutError("private engine detail")

        monkeypatch.setattr(TuViService, "generate_full_chart", fail)
        safe_client = TestClient(app, raise_server_exceptions=False)
        response = safe_client.post("/chart/generate", json=BIRTH)
        assert response.status_code == 503
        assert response.json()["error"] == "Chart engine unavailable"
        assert "private engine detail" not in response.text

    def test_default_cors_does_not_enable_credentials(self):
        response = client.options(
            "/health",
            headers={
                "Origin": "https://example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert response.headers["Access-Control-Allow-Origin"] == "*"
        assert "Access-Control-Allow-Credentials" not in response.headers


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
