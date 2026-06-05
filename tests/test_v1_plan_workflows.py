import pytest
from fastapi.testclient import TestClient

import civicplan.main as main_module
from civicplan.integration_mocks import CivicPlanIntegrationMockLayer, IntegrationError
from civicplan.main import app


client = TestClient(app)
STAFF_HEADERS = {"X-CivicPlan-Role": "staff", "X-CivicPlan-Staff-Key": "test-staff-key"}


@pytest.fixture(autouse=True)
def reset_policy_repository() -> None:
    main_module._dispose_policy_repository()


def test_plan_navigator_groups_policy_structure() -> None:
    response = client.get("/api/v1/civicplan/plans/navigator")

    assert response.status_code == 200
    payload = response.json()
    plan_types = {plan["plan_type"] for plan in payload["plans"]}
    policy_ids = {
        policy["policy_id"]
        for plan in payload["plans"]
        for policy in plan["policies"]
    }
    assert {"comprehensive", "transportation", "parks"} <= plan_types
    assert {
        "comp-plan-housing-2.1",
        "transportation-plan-3.4",
        "parks-plan-1.2",
    } <= policy_ids
    assert "staff verify applicability" in payload["boundary"]


def test_plan_question_answer_and_synthesis_are_cited_and_review_required() -> None:
    answer = client.post(
        "/api/v1/civicplan/questions/answer",
        json={"question": "What does the plan say about missing middle housing?"},
    )
    synthesis = client.post(
        "/api/v1/civicplan/plans/synthesis",
        json={"topic": "housing affordability near parks and services"},
    )

    assert answer.status_code == 200
    assert answer.json()["status"] == "answered"
    assert answer.json()["review_required"] is True
    assert answer.json()["citations"]
    assert len(answer.json()["source_policy_ids"]) == len(set(answer.json()["source_policy_ids"]))
    assert synthesis.status_code == 200
    assert synthesis.json()["review_required"] is True
    assert synthesis.json()["citations"]


def test_amendment_history_distinguishes_pending_from_adopted() -> None:
    response = client.get("/api/v1/civicplan/amendments/history")

    assert response.status_code == 200
    statuses = {item["adoption_status"] for item in response.json()["items"]}
    assert {"adopted", "pending"} <= statuses
    assert "Pending amendments are not treated as adopted" in response.json()["boundary"]


def test_progress_targets_return_evidence_and_boundary() -> None:
    response = client.get("/api/v1/civicplan/progress/targets?policy_id=parks-plan-1.2")

    assert response.status_code == 200
    payload = response.json()
    assert payload["items"][0]["policy_id"] == "parks-plan-1.2"
    assert payload["items"][0]["evidence"]
    assert "not official findings" in payload["boundary"]


def test_civicclerk_context_is_draft_only_and_cited() -> None:
    response = client.post(
        "/api/v1/civicplan/context/civicclerk",
        json={"agenda_item": "North corridor rezoning staff report", "topic": "housing"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["review_required"] is True
    assert payload["citations"]
    assert "draft-only" in payload["boundary"]


def test_staff_policy_ingestion_requires_database_and_persists(tmp_path, monkeypatch) -> None:
    no_db = client.post(
        "/api/v1/civicplan/policies/ingest",
        json=_ingest_payload(),
        headers=STAFF_HEADERS,
    )
    db_url = f"sqlite+pysqlite:///{tmp_path / 'policies.db'}"
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", db_url)
    monkeypatch.setenv("CIVICPLAN_STAFF_API_KEY", "test-staff-key")
    created = client.post(
        "/api/v1/civicplan/policies/ingest",
        json=_ingest_payload(),
        headers=STAFF_HEADERS,
    )
    main_module._dispose_policy_repository()
    found = client.post(
        "/api/v1/civicplan/policies/lookup",
        json={"topic": "resilience", "plan_type": "sustainability"},
    )

    assert no_db.status_code == 503
    assert "Set CIVICPLAN_POLICY_DB_URL" in no_db.json()["detail"]["fix"]
    assert created.status_code == 200
    assert created.json()["policy"]["policy_id"] == "sustainability-plan-4.2"
    assert found.status_code == 200
    assert found.json()["policy_id"] == "sustainability-plan-4.2"


def test_policy_ingestion_labels_pending_language(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", f"sqlite+pysqlite:///{tmp_path / 'pending.db'}")
    monkeypatch.setenv("CIVICPLAN_STAFF_API_KEY", "test-staff-key")
    payload = _ingest_payload()
    payload["adoption_status"] = "pending"

    created = client.post(
        "/api/v1/civicplan/policies/ingest",
        json=payload,
        headers=STAFF_HEADERS,
    )

    assert created.status_code == 200
    assert created.json()["adoption_status"] == "pending"
    assert "pending" in created.json()["policy"]["relevance"]


def test_integration_mocks_reject_live_endpoints_and_malformed_payloads() -> None:
    layer = CivicPlanIntegrationMockLayer()
    live = layer.run("geojson_area_boundary", {"url": "https://example.test/geojson"})
    malformed = layer.run("local_plan_document_import", {"policies": []})
    ok = layer.run(
        "civicclerk_staff_report_context",
        {"agenda_item": "Housing hearing", "staff_report_id": "sr-1"},
    )

    assert isinstance(live, IntegrationError)
    assert live.code == "air_gap_violation"
    assert isinstance(malformed, IntegrationError)
    assert malformed.code == "malformed_payload"
    assert not isinstance(ok, IntegrationError)
    assert ok.records[0]["visibility"] == "staff_only"


def _ingest_payload() -> dict[str, str]:
    return {
        "topic_key": "resilience",
        "policy_id": "sustainability-plan-4.2",
        "plan_type": "sustainability",
        "title": "Heat resilience corridors",
        "citation": "Sustainability Plan, Climate Chapter, Policy C-4.2",
        "excerpt": "Prioritize shade, cool pavement, and emergency cooling access in heat-vulnerable corridors.",
        "relevance": "Relevant for street redesign, park investment, and capital planning.",
        "adoption_status": "adopted",
        "source_document": "2025 Sustainability Plan",
    }
