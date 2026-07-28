"""
Advanced API endpoint tests for new features
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestChartAnalysisEndpoints:
    """Test chart analysis endpoints"""

    def test_chart_analyze_success(self):
        """Test successful chart analysis"""
        response = client.post(
            "/chart/analyze",
            json={
                "ngay": 15,
                "thang": 8,
                "nam": 1990,
                "gio": 7,
                "gioi_tinh": 1,
                "duong_lich": True,
                "timezone": 7,
            },
        )

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert "birth_info" in data
        assert "life_palace_analysis" in data
        assert "career_palace_analysis" in data
        assert "wealth_palace_analysis" in data
        assert "overall_strength" in data
        assert "lucky_elements" in data
        assert "unlucky_elements" in data
        assert "major_life_events" in data
        assert "generated_at" in data

    def test_chart_analyze_with_name(self):
        """Test chart analysis with person's name"""
        response = client.post(
            "/chart/analyze",
            json={
                "ngay": 20,
                "thang": 12,
                "nam": 1995,
                "gio": 3,
                "gioi_tinh": -1,
                "duong_lich": True,
                "ten": "Test Person",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["birth_info"]["ten"] == "Test Person"

    def test_chart_analyze_invalid_data(self):
        """Test chart analysis with invalid data"""
        response = client.post(
            "/chart/analyze",
            json={
                "ngay": 35,  # Invalid day
                "thang": 8,
                "nam": 1990,
                "gio": 7,
                "gioi_tinh": 1,
                "duong_lich": True,
            },
        )

        assert response.status_code == 422  # Validation error


class TestBatchChartGeneration:
    """Test batch chart generation endpoint"""

    def test_batch_generate_success(self):
        """Test successful batch chart generation"""
        response = client.post(
            "/chart/batch",
            json={
                "charts": [
                    {
                        "ngay": 15,
                        "thang": 8,
                        "nam": 1990,
                        "gio": 7,
                        "gioi_tinh": 1,
                        "duong_lich": True,
                        "ten": "Person 1",
                    },
                    {
                        "ngay": 20,
                        "thang": 12,
                        "nam": 1995,
                        "gio": 3,
                        "gioi_tinh": -1,
                        "duong_lich": True,
                        "ten": "Person 2",
                    },
                ]
            },
        )

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "results" in data
        assert "total" in data
        assert "successful" in data
        assert "failed" in data
        assert "generated_at" in data

        # Check we got 2 results
        assert data["total"] == 2
        assert data["successful"] == 2
        assert len(data["results"]) == 2

        # Check each result has required fields
        for result in data["results"]:
            assert "birth_info" in result
            assert "lunar_date" in result
            assert "can_chi" in result
            assert "dia_ban" in result

    def test_batch_generate_max_limit(self):
        """Test batch generation with max limit (10 charts)"""
        charts = []
        for i in range(10):
            charts.append(
                {
                    "ngay": 1 + i,
                    "thang": 1,
                    "nam": 1990,
                    "gio": 1,
                    "gioi_tinh": 1 if i % 2 == 0 else -1,
                    "duong_lich": True,
                    "ten": f"Person {i + 1}",
                }
            )

        response = client.post("/chart/batch", json={"charts": charts})

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 10
        assert data["successful"] == 10
        assert len(data["results"]) == 10

    def test_batch_generate_exceeds_limit(self):
        """Test batch generation exceeding limit"""
        charts = []
        for i in range(15):  # More than max 10
            charts.append(
                {
                    "ngay": 1,
                    "thang": 1,
                    "nam": 1990,
                    "gio": 1,
                    "gioi_tinh": 1,
                    "duong_lich": True,
                }
            )

        response = client.post("/chart/batch", json={"charts": charts})

        # Pydantic validation will return 422 for constraint violation
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_batch_generate_empty_list(self):
        """Test batch generation with empty chart list"""
        response = client.post("/chart/batch", json={"charts": []})

        # Pydantic validation will return 422 for constraint violation
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_batch_generate_one_invalid(self):
        """Test batch generation with one invalid chart"""
        response = client.post(
            "/chart/batch",
            json={
                "charts": [
                    {
                        "ngay": 15,
                        "thang": 8,
                        "nam": 1990,
                        "gio": 7,
                        "gioi_tinh": 1,
                        "duong_lich": True,
                    },
                    {
                        "ngay": 35,  # Invalid
                        "thang": 8,
                        "nam": 1990,
                        "gio": 7,
                        "gioi_tinh": 1,
                        "duong_lich": True,
                    },
                ]
            },
        )

        # Should still fail validation
        assert response.status_code == 422


class TestInfoEndpoints:
    """Test information endpoints"""

    def test_elements_info(self):
        """Test Five Elements info endpoint"""
        response = client.get("/info/elements")

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "title" in data
        assert "description" in data
        assert "elements" in data
        assert "cycle" in data

        # Check we have 5 elements
        assert len(data["elements"]) == 5

        # Check each element has required fields
        for elem in data["elements"]:
            assert "id" in elem
            assert "key" in elem
            assert "name" in elem
            assert "cuc" in elem
            assert "ten_cuc" in elem

        # Check cycles
        assert "generation" in data["cycle"]
        assert "destruction" in data["cycle"]

    def test_can_chi_info(self):
        """Test Can Chi info endpoint"""
        response = client.get("/info/can-chi")

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "title" in data
        assert "thien_can" in data
        assert "dia_chi" in data

        # Check Thien Can (10 stems)
        assert "thien_can" in data
        assert data["thien_can"]["count"] == 10
        assert len(data["thien_can"]["items"]) == 10
        for can in data["thien_can"]["items"]:
            assert "id" in can
            assert "name" in can
            # Element may be present but is optional

        # Check Dia Chi (12 branches)
        assert "dia_chi" in data
        assert data["dia_chi"]["count"] == 12
        assert len(data["dia_chi"]["items"]) == 12
        for chi in data["dia_chi"]["items"]:
            assert "id" in chi
            assert "name" in chi
            # Zodiac and element may be present but are optional

    def test_stats_endpoint(self):
        """Test API statistics endpoint"""
        response = client.get("/stats")

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "api_version" in data
        assert "status" in data
        assert "endpoints" in data
        assert "features" in data

        # Check endpoints count
        assert data["endpoints"]["total"] > 0
        assert "chart_generation" in data["endpoints"]
        assert "calendar" in data["endpoints"]
        assert "analysis" in data["endpoints"]
        assert "info" in data["endpoints"]

        # Check features list
        assert isinstance(data["features"], list)
        assert len(data["features"]) > 0


class TestMiddleware:
    """Test API middleware functionality"""

    def test_process_time_header(self):
        """Test that X-Process-Time header is added"""
        response = client.get("/health")

        assert response.status_code == 200
        assert "x-process-time" in response.headers
        # Process time should be a number
        process_time = float(response.headers["x-process-time"])
        assert process_time >= 0

    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = client.options(
            "/health",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "GET",
            },
        )

        # Check CORS headers
        assert "access-control-allow-origin" in response.headers

    def test_error_handling(self):
        """Test global error handling"""
        # Try to access non-existent endpoint
        response = client.get("/non-existent")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data


class TestValidation:
    """Test request validation"""

    def test_invalid_date(self):
        """Test invalid date validation"""
        response = client.post(
            "/chart/generate",
            json={
                "ngay": 32,  # Invalid day
                "thang": 1,
                "nam": 1990,
                "gio": 7,
                "gioi_tinh": 1,
                "duong_lich": True,
            },
        )

        assert response.status_code == 422

    def test_invalid_hour(self):
        """Test invalid hour validation"""
        response = client.post(
            "/chart/generate",
            json={
                "ngay": 15,
                "thang": 8,
                "nam": 1990,
                "gio": 13,  # Invalid hour (must be 1-12)
                "gioi_tinh": 1,
                "duong_lich": True,
            },
        )

        assert response.status_code == 422

    def test_invalid_gender(self):
        """Test invalid gender validation"""
        response = client.post(
            "/chart/generate",
            json={
                "ngay": 15,
                "thang": 8,
                "nam": 1990,
                "gio": 7,
                "gioi_tinh": 2,  # Invalid (must be 1 or -1)
                "duong_lich": True,
            },
        )

        assert response.status_code == 422

    def test_missing_required_fields(self):
        """Test missing required fields"""
        response = client.post(
            "/chart/generate",
            json={
                "ngay": 15,
                "thang": 8,
                # Missing nam, gio, gioi_tinh, duong_lich
            },
        )

        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
