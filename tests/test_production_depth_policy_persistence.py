from fastapi.testclient import TestClient

import civicplan.main as main_module
from civicplan.main import app
from civicplan.persistence import PlanPolicyRepository


client = TestClient(app)


def test_policy_and_staff_analysis_records_persist(tmp_path) -> None:
    db_path = tmp_path / "policy-records.db"
    repository = PlanPolicyRepository(db_url=f"sqlite:///{db_path}")

    policy = repository.lookup_policy(topic="housing", plan_type="comprehensive")
    stored = repository.create_staff_analysis(
        project_name="Maple Avenue Homes",
        proposal="Housing near transit and sidewalks.",
        policy_id="housing",
    )
    repository.engine.dispose()

    second_repository = PlanPolicyRepository(db_url=f"sqlite:///{db_path}", seed_defaults=False)
    try:
        reloaded_policy = second_repository.lookup_policy(topic="housing")
        reloaded_analysis = second_repository.get_staff_analysis(stored.analysis_id)
    finally:
        second_repository.engine.dispose()

    assert reloaded_policy == policy
    assert reloaded_analysis is not None
    assert reloaded_analysis.heading == "Plan consistency context for Maple Avenue Homes"
    assert "Comprehensive Plan, Housing Element, Policy H-2.1" in reloaded_analysis.citations
    db_path.unlink()


def test_api_uses_configured_policy_database(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "api-policy-records.db"
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", f"sqlite:///{db_path}")

    try:
        policy_response = client.post(
            "/api/v1/civicplan/policies/lookup",
            json={"topic": "housing", "plan_type": "comprehensive"},
        )
        create_response = client.post(
            "/api/v1/civicplan/staff-analysis/draft",
            json={
                "project_name": "Maple Avenue Homes",
                "proposal": "Housing near transit and sidewalks.",
                "policy_id": "housing",
            },
        )
        analysis_id = create_response.json()["analysis_id"]
        get_response = client.get(f"/api/v1/civicplan/staff-analysis/{analysis_id}")
    finally:
        main_module._dispose_policy_repository()
        main_module._policy_db_url = None

    assert policy_response.status_code == 200
    assert policy_response.json()["policy_id"] == "comp-plan-housing-2.1"
    assert create_response.status_code == 200
    assert analysis_id
    assert get_response.status_code == 200
    assert get_response.json()["analysis_id"] == analysis_id
    assert get_response.json()["review_required"] is True
    db_path.unlink()


def test_staff_analysis_lookup_requires_configured_database() -> None:
    response = client.get("/api/v1/civicplan/staff-analysis/not-configured")

    assert response.status_code == 503
    assert "Set CIVICPLAN_POLICY_DB_URL" in response.json()["detail"]["fix"]
