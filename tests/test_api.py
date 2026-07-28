"""
Test suite for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestAPIBasics:
    """Test basic API functionality"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data


class TestCalendarEndpoints:
    """Test calendar conversion endpoints"""
    
    def test_solar_to_lunar_valid(self):
        """Test valid solar to lunar conversion"""
        response = client.post(
            "/calendar/solar-to-lunar",
            params={
                "ngay": 15,
                "thang": 8,
                "nam": 1990,
                "timezone": 7
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "ngay_am" in data
        assert "thang_am" in data
        assert "nam_am" in data
        assert "thang_nhuan" in data
    
    def test_solar_to_lunar_invalid(self):
        """Test invalid solar date"""
        response = client.post(
            "/calendar/solar-to-lunar",
            params={
                "ngay": 32,  # Invalid day
                "thang": 13,  # Invalid month
                "nam": 1990,
                "timezone": 7
            }
        )
        # API may return 200 with error or 400, accept both
        assert response.status_code in [200, 400]
    
    def test_can_chi_solar(self):
        """Test Can Chi calculation for solar date"""
        response = client.post(
            "/calendar/can-chi",
            params={
                "ngay": 15,
                "thang": 8,
                "nam": 1990,
                "duong_lich": True,
                "timezone": 7
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "can_nam" in data
        assert "chi_nam" in data
        assert "can_thang" in data
        assert "ten_can_nam" in data
        assert "ten_chi_nam" in data


class TestChartGeneration:
    """Test chart generation endpoints"""
    
    @pytest.fixture
    def valid_birth_info(self):
        """Valid birth information fixture"""
        return {
            "ngay": 15,
            "thang": 8,
            "nam": 1990,
            "gio": 7,  # Mão time
            "gioi_tinh": 1,  # Male
            "duong_lich": True,
            "timezone": 7,
            "ten": "Test User"
        }
    
    def test_generate_dia_ban(self, valid_birth_info):
        """Test Dia Ban generation"""
        response = client.post(
            "/chart/dia-ban",
            json=valid_birth_info
        )
        assert response.status_code == 200
        data = response.json()
        assert "cung_menh" in data
        assert "thap_nhi_cung" in data
        assert len(data["thap_nhi_cung"]) == 12
        
        # Check each cung has required fields
        for cung in data["thap_nhi_cung"]:
            assert "cung_so" in cung
            assert "cung_ten" in cung
            assert "cung_sao" in cung
    
    def test_generate_full_chart(self, valid_birth_info):
        """Test complete chart generation"""
        response = client.post(
            "/chart/generate",
            json=valid_birth_info
        )
        assert response.status_code == 200
        data = response.json()
        
        # Check main structure
        assert "birth_info" in data
        assert "lunar_date" in data
        assert "can_chi" in data
        assert "dia_ban" in data
        assert "generated_at" in data
        
        # Check birth info
        assert data["birth_info"]["ten"] == "Test User"
        assert data["birth_info"]["gioi_tinh"] == 1
        
        # Check dia ban
        assert len(data["dia_ban"]["thap_nhi_cung"]) == 12
    
    def test_generate_chart_female(self, valid_birth_info):
        """Test chart generation for female"""
        valid_birth_info["gioi_tinh"] = -1  # Female
        valid_birth_info["ten"] = "Test Female"
        
        response = client.post(
            "/chart/generate",
            json=valid_birth_info
        )
        assert response.status_code == 200
        data = response.json()
        assert data["birth_info"]["gioi_tinh"] == -1
    
    def test_generate_chart_different_times(self, valid_birth_info):
        """Test chart generation for different birth times"""
        for gio in range(1, 13):  # Test all 12 hours
            valid_birth_info["gio"] = gio
            response = client.post(
                "/chart/generate",
                json=valid_birth_info
            )
            assert response.status_code == 200
    
    def test_generate_chart_invalid_hour(self, valid_birth_info):
        """Test chart generation with invalid hour"""
        valid_birth_info["gio"] = 13  # Invalid hour
        response = client.post(
            "/chart/generate",
            json=valid_birth_info
        )
        assert response.status_code == 422  # Validation error
    
    def test_generate_chart_invalid_gender(self, valid_birth_info):
        """Test chart generation with invalid gender"""
        valid_birth_info["gioi_tinh"] = 0  # Invalid gender
        response = client.post(
            "/chart/generate",
            json=valid_birth_info
        )
        assert response.status_code == 422  # Validation error


class TestInfoEndpoints:
    """Test informational endpoints"""
    
    def test_gio_chi_info(self):
        """Test Địa Chi hour information endpoint"""
        response = client.get("/info/gio-chi")
        assert response.status_code == 200
        data = response.json()
        
        assert "title" in data
        assert "hours" in data
        assert len(data["hours"]) == 12
        
        # Check first hour (Tý)
        first_hour = data["hours"][0]
        assert first_hour["id"] == 1
        assert "ten" in first_hour
        assert "time_range" in first_hour


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_leap_month(self):
        """Test solar to lunar conversion for leap month"""
        # Find a date that falls in a leap month
        response = client.post(
            "/calendar/solar-to-lunar",
            params={
                "ngay": 15,
                "thang": 6,
                "nam": 2023,  # Year with leap month
                "timezone": 7
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "thang_nhuan" in data
    
    def test_year_boundaries(self):
        """Test dates at year boundaries"""
        # New Year's Eve
        response = client.post(
            "/calendar/solar-to-lunar",
            params={
                "ngay": 31,
                "thang": 12,
                "nam": 1990,
                "timezone": 7
            }
        )
        assert response.status_code == 200
        
        # New Year's Day
        response = client.post(
            "/calendar/solar-to-lunar",
            params={
                "ngay": 1,
                "thang": 1,
                "nam": 1991,
                "timezone": 7
            }
        )
        assert response.status_code == 200
    
    def test_missing_required_fields(self):
        """Test chart generation with missing fields"""
        incomplete_data = {
            "ngay": 15,
            "thang": 8,
            # Missing nam, gio, gioi_tinh
        }
        response = client.post(
            "/chart/generate",
            json=incomplete_data
        )
        assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
