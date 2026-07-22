import json
from pathlib import Path


def test_report_file_exists():
    """The task must create /app/report.json."""
    assert Path("/app/report.json").exists(), "Expected /app/report.json to exist."


def test_report_is_valid_json():
    """The report must be valid JSON."""
    report_path = Path("/app/report.json")
    with report_path.open("r", encoding="utf-8") as f:
        report = json.load(f)
    assert isinstance(report, dict), "report.json must contain a JSON object"


def test_report_has_required_fields():
    """The report must include the required summary fields."""
    report = json.loads(Path("/app/report.json").read_text(encoding="utf-8"))
    expected_fields = [
        "total_requests",
        "unique_ips",
        "top_path",
        "top_paths",
        "methods",
        "status_codes",
    ]
    for field in expected_fields:
        assert field in report, f"Missing required field: {field}"


def test_report_counts_are_correct():
    """The report must count requests, IPs, methods, and status codes correctly."""
    report = json.loads(Path("/app/report.json").read_text(encoding="utf-8"))
    assert report["total_requests"] == 6, "total_requests should be 6"
    assert report["unique_ips"] == 3, "unique_ips should be 3"
    assert report["top_path"] == "/index.html", "top_path should be /index.html"
    assert report["methods"]["GET"] == 5, "GET request count should be 5"
    assert report["methods"]["POST"] == 1, "POST request count should be 1"
    assert report["status_codes"]["200"] == 5, "200 status count should be 5"
    assert report["status_codes"]["401"] == 1, "401 status count should be 1"
