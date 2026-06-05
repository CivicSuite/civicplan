import subprocess
import sys

from fastapi.testclient import TestClient

import civicplan.main as main_module
from civicplan.main import app
from civicplan.persistence import SCHEMA_VERSION, PlanPolicyRepository
from civicplan.policy_lookup import PlanPolicy


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
    db_path.unlink(missing_ok=True)


def test_policy_repository_records_schema_status(tmp_path) -> None:
    db_path = tmp_path / "schema-status.db"
    repository = PlanPolicyRepository(db_url=f"sqlite:///{db_path}", seed_defaults=False)
    try:
        status = repository.schema_status()
    finally:
        repository.engine.dispose()

    assert status.ready is True
    assert status.schema_version == SCHEMA_VERSION
    assert status.expected_schema_version == SCHEMA_VERSION
    assert status.missing_tables == ()
    assert status.dialect == "sqlite"


def test_db_status_cli_reports_ready_schema(tmp_path) -> None:
    db_path = tmp_path / "schema-cli.db"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "civicplan.db_admin",
            "--db-url",
            f"sqlite:///{db_path}",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "CivicPlan schema ready" in result.stdout
    assert f"version={SCHEMA_VERSION}" in result.stdout
    assert "missing_tables=none" in result.stdout


def test_api_uses_configured_policy_database(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "api-policy-records.db"
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("CIVICPLAN_STAFF_API_KEY", "test-staff-key")
    staff_headers = {"X-CivicPlan-Role": "staff", "X-CivicPlan-Staff-Key": "test-staff-key"}

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
            headers=staff_headers,
        )
        analysis_id = create_response.json()["analysis_id"]
        get_response = client.get(
            f"/api/v1/civicplan/staff-analysis/{analysis_id}",
            headers=staff_headers,
        )
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
    db_path.unlink(missing_ok=True)


def test_readiness_requires_configured_policy_database() -> None:
    response = client.get("/api/v1/civicplan/readiness")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "not-ready"
    assert payload["ready"] is False
    assert payload["policy_database_configured"] is False
    assert "Set CIVICPLAN_POLICY_DB_URL" in payload["blockers"][0]


def test_configured_runtime_does_not_seed_sample_policies(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "empty-runtime.db"
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", f"sqlite:///{db_path}")

    try:
        response = client.get("/ready")
        repository = main_module._get_policy_repository()
        policies = repository.list_policies()
    finally:
        main_module._dispose_policy_repository()
        main_module._policy_db_url = None

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "not-ready"
    assert payload["schema_ready"] is True
    assert payload["policy_count"] == 0
    assert "Load adopted municipal plan policies" in payload["blockers"][0]
    assert policies == ()


def test_readiness_passes_with_loaded_local_policies(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "ready-runtime.db"
    db_url = f"sqlite:///{db_path}"
    repository = PlanPolicyRepository(db_url=db_url, seed_defaults=False)
    repository.upsert_policy(
        topic_key="resilience",
        policy=PlanPolicy(
            policy_id="sustainability-plan-4.2",
            plan_type="sustainability",
            title="Heat resilience corridors",
            citation="Sustainability Plan, Climate Chapter, Policy C-4.2",
            excerpt="Prioritize shade, cool pavement, and emergency cooling access.",
            relevance="Relevant for local heat-resilience capital planning.",
        ),
    )
    repository.engine.dispose()
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", db_url)

    try:
        response = client.get("/api/v1/civicplan/readiness")
    finally:
        main_module._dispose_policy_repository()
        main_module._policy_db_url = None

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    assert payload["ready"] is True
    assert payload["policy_database_configured"] is True
    assert payload["schema_ready"] is True
    assert payload["policy_count"] == 1
    assert payload["blockers"] == []


def test_persisted_staff_analysis_requires_staff_role(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "staff-auth.db"
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("CIVICPLAN_STAFF_API_KEY", "test-staff-key")

    try:
        create_response = client.post(
            "/api/v1/civicplan/staff-analysis/draft",
            json={
                "project_name": "Maple Avenue Homes",
                "proposal": "CONFIDENTIAL: acquire parcel 123 before public notice.",
                "policy_id": "housing",
            },
        )
        get_response = client.get("/api/v1/civicplan/staff-analysis/not-authorized")
    finally:
        main_module._dispose_policy_repository()
        main_module._policy_db_url = None

    assert create_response.status_code == 403
    assert get_response.status_code == 403
    assert "X-CivicPlan-Role: staff" in create_response.json()["detail"]["fix"]
    db_path.unlink(missing_ok=True)


def test_staff_analysis_rejects_oversized_persisted_proposal(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "staff-validation.db"
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("CIVICPLAN_STAFF_API_KEY", "test-staff-key")

    try:
        response = client.post(
            "/api/v1/civicplan/staff-analysis/draft",
            json={
                "project_name": "Maple Avenue Homes",
                "proposal": "x" * 5001,
                "policy_id": "housing",
            },
            headers={"X-CivicPlan-Role": "staff", "X-CivicPlan-Staff-Key": "test-staff-key"},
        )
    finally:
        main_module._dispose_policy_repository()
        main_module._policy_db_url = None

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert "proposal" in detail["fields"]
    assert "fields array" in detail["fix"]
    db_path.unlink(missing_ok=True)


def test_zoning_context_api_uses_configured_policy_database(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "api-policy-context.db"
    db_url = f"sqlite:///{db_path}"
    repository = PlanPolicyRepository(db_url=db_url, seed_defaults=False)
    repository.seed_policies(
        [
            (
                "accessory dwelling unit",
                PlanPolicy(
                    policy_id="housing-adu-4.2",
                    plan_type="housing",
                    title="ADU compatibility near services",
                    citation="Housing Plan, Policy H-4.2",
                    excerpt="Support accessory dwelling units where services and adopted design standards are available.",
                    relevance="Relevant when CivicZone asks for ADU policy context.",
                ),
            )
        ]
    )
    repository.engine.dispose()
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", db_url)

    try:
        response = client.post(
            "/api/v1/civicplan/context/zoning",
            json={
                "topic": "accessory dwelling unit",
                "zone_code": "R-2",
                "use": "ADU",
                "plan_type": "housing",
                "civiczone_context_id": "ledger-1",
            },
        )
    finally:
        main_module._dispose_policy_repository()
        main_module._policy_db_url = None

    assert response.status_code == 200
    payload = response.json()
    assert payload["policy_id"] == "housing-adu-4.2"
    assert payload["citation"] == "Housing Plan, Policy H-4.2"
    assert payload["source"] == "persisted"
    assert payload["review_required"] is True
    assert payload["civiczone_context_id"] == "ledger-1"
    db_path.unlink()


def test_zoning_context_persisted_lookup_does_not_match_plan_type_only(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "api-policy-context-scope.db"
    db_url = f"sqlite:///{db_path}"
    repository = PlanPolicyRepository(db_url=db_url, seed_defaults=False)
    repository.seed_policies(
        [
            (
                "industrial expansion",
                PlanPolicy(
                    policy_id="industrial-1",
                    plan_type="housing",
                    title="Industrial transition policy",
                    citation="Housing Plan, Policy I-1",
                    excerpt="Review industrial transition areas before residential conversion.",
                    relevance="Not relevant to an ADU question.",
                ),
            ),
            (
                "accessory dwelling unit",
                PlanPolicy(
                    policy_id="housing-adu-4.2",
                    plan_type="housing",
                    title="ADU compatibility near services",
                    citation="Housing Plan, Policy H-4.2",
                    excerpt="Support accessory dwelling units where services and adopted design standards are available.",
                    relevance="Relevant when CivicZone asks for ADU policy context.",
                ),
            ),
        ]
    )
    repository.engine.dispose()
    monkeypatch.setenv("CIVICPLAN_POLICY_DB_URL", db_url)

    try:
        response = client.post(
            "/api/v1/civicplan/context/zoning",
            json={
                "topic": "accessory dwelling unit",
                "zone_code": "R-2",
                "use": "ADU",
                "plan_type": "housing",
            },
        )
    finally:
        main_module._dispose_policy_repository()
        main_module._policy_db_url = None

    assert response.status_code == 200
    payload = response.json()
    assert payload["policy_id"] == "housing-adu-4.2"
    assert payload["policy_id"] != "industrial-1"
    assert payload["source"] == "persisted"
    db_path.unlink()


def test_staff_analysis_lookup_requires_configured_database() -> None:
    response = client.get("/api/v1/civicplan/staff-analysis/not-configured")

    assert response.status_code == 503
    assert "Set CIVICPLAN_POLICY_DB_URL" in response.json()["detail"]["fix"]
