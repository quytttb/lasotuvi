"""Test suite for FastAPI endpoints (English schema v2)."""
import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


class TestAPIBasics:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "2.0.0"

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestCalendarEndpoints:
    def test_solar_to_lunar_valid(self):
        response = client.post(
            "/calendar/solar-to-lunar",
            params={"day": 15, "month": 8, "year": 1990, "timezone": 7},
        )
        assert response.status_code == 200
        data = response.json()
        assert "day" in data and "month" in data and "year" in data
        assert "is_leap_month" in data

    def test_lunar_to_solar_roundtrip(self):
        lunar = client.post(
            "/calendar/solar-to-lunar",
            params={"day": 15, "month": 8, "year": 1990, "timezone": 7},
        ).json()
        solar = client.post(
            "/calendar/lunar-to-solar",
            params={
                "day": lunar["day"],
                "month": lunar["month"],
                "year": lunar["year"],
                "is_leap_month": lunar["is_leap_month"],
                "timezone": 7,
            },
        )
        assert solar.status_code == 200
        data = solar.json()
        assert data["day"] == 15
        assert data["month"] == 8
        assert data["year"] == 1990

    def test_stem_branch(self):
        response = client.post(
            "/calendar/stem-branch",
            params={
                "day": 15,
                "month": 8,
                "year": 1990,
                "is_solar": True,
                "timezone": 7,
                "hour": 7,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["year"]["label"]
        assert data["hour"]["branch"] == 7


class TestChartGeneration:
    @pytest.fixture
    def birth(self):
        return {
            "day": 15,
            "month": 8,
            "year": 1990,
            "hour": 7,
            "gender": 1,
            "is_solar": True,
            "timezone": 7,
            "name": "Test User",
            "view_year": 2026,
        }

    def test_generate_earth_plate(self, birth):
        response = client.post("/chart/earth-plate", json=birth)
        assert response.status_code == 200
        data = response.json()
        assert "life_palace" in data
        assert len(data["palaces"]) == 12
        for palace in data["palaces"]:
            assert "index" in palace
            assert "branch_name" in palace
            assert "stars" in palace
            assert "monthly_luck" in palace

    def test_generate_full_chart(self, birth):
        response = client.post("/chart/generate", json=birth)
        assert response.status_code == 200
        data = response.json()
        assert data["birth_info"]["name"] == "Test User"
        assert data["stem_branch"]["year"]["label"]
        assert data["chart_meta"]["life_master"]
        assert data["chart_meta"]["view_year"] == 2026
        assert "formations" in data
        assert "formations" in data["earth_plate"]
        palace = data["earth_plate"]["palaces"][0]
        assert "interpretations" in palace
        if palace["stars"]:
            star = palace["stars"][0]
            assert "id" in star and "name" in star
            assert "is_auspicious" in star

    def test_generate_chart_female(self, birth):
        birth["gender"] = -1
        response = client.post("/chart/generate", json=birth)
        assert response.status_code == 200
        assert response.json()["birth_info"]["gender"] == -1

    def test_invalid_hour(self, birth):
        birth["hour"] = 13
        assert client.post("/chart/generate", json=birth).status_code == 422

    def test_invalid_gender(self, birth):
        birth["gender"] = 0
        assert client.post("/chart/generate", json=birth).status_code == 422


class TestInfoEndpoints:
    def test_hour_branches(self):
        response = client.get("/info/hour-branches")
        assert response.status_code == 200
        data = response.json()
        assert len(data["hours"]) == 12
        assert data["hours"][0]["time_range"] == "23h - 1h"

    def test_star_catalog(self):
        response = client.get("/info/stars")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 100
        assert "brightness" in data
