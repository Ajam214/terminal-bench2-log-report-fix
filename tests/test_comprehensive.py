import json
from pathlib import Path
import pytest


def test_report_exists():
    """Report file should exist."""
    assert Path("/app/report.json").exists()


def test_report_nonempty():
    """Report file should not be empty."""
    assert Path("/app/report.json").stat().st_size > 0


@pytest.fixture
def report():
    with open("/app/report.json") as f:
        return json.load(f)


class TestReportFields:
    def test_has_required_fields(self, report):
        required = ["total_requests", "unique_ips", "top_path"]
        for field in required:
            assert field in report, f"Missing field: {field}"
    
    def test_has_enhanced_fields(self, report):
        # Should have the extra stats too
        assert "top_paths" in report
        assert "methods" in report
        assert "status_codes" in report
    
    def test_total_requests_positive(self, report):
        assert report["total_requests"] > 0
    
    def test_unique_ips_positive(self, report):
        assert report["unique_ips"] > 0
    
    def test_top_path_not_none(self, report):
        assert report["top_path"] is not None


class TestDataTypes:
    def test_top_paths_is_list(self, report):
        assert isinstance(report["top_paths"], list)
    
    def test_methods_is_dict(self, report):
        assert isinstance(report["methods"], dict)
    
    def test_status_codes_is_dict(self, report):
        assert isinstance(report["status_codes"], dict)


class TestValues:
    def test_correct_total(self, report):
        # Should have 6 requests from the test log
        assert report["total_requests"] == 6
    
    def test_correct_ips(self, report):
        # Should have 3 unique IPs
        assert report["unique_ips"] == 3
    
    def test_top_path_is_index(self, report):
        assert report["top_path"] == "/index.html"
    
    def test_get_requests_count(self, report):
        assert report["methods"]["GET"] == 5
    
    def test_post_requests_count(self, report):
        assert report["methods"]["POST"] == 1
    
    def test_status_200_count(self, report):
        assert report["status_codes"]["200"] == 5
    
    def test_status_401_count(self, report):
        assert report["status_codes"]["401"] == 1
