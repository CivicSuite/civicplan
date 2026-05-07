from fastapi.testclient import TestClient

import civicplan
from civicplan.main import app


client = TestClient(app)


def test_package_version_is_100() -> None:
    assert civicplan.__version__ == "1.0.0"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicPlan"
    assert payload["version"] == "1.0.0"
    assert payload["status"] == "v1 cited planning policy and staff analysis runtime"
    assert "staff-only local policy ingestion" in payload["message"]
    assert "CivicZone and CivicClerk context contracts" in payload["message"]
    assert "does not make official planning determinations" in payload["message"]
    assert payload["next_step"].startswith("Configure local plan policies")


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civicplan"
    assert payload["version"] == "1.0.0"
    assert payload["civiccore_version"] == "1.0.0"
