from __future__ import annotations

import pytest

from civicplan.data_import import import_local_policies
from civicplan.persistence import PlanPolicyRepository


def test_local_policy_import_loads_policies_without_samples(tmp_path) -> None:
    db_url = f"sqlite:///{tmp_path / 'policies.db'}"
    policies_csv = tmp_path / "policies.csv"
    policies_csv.write_text(
        "\n".join(
            [
                (
                    "topic_key,policy_id,plan_type,title,citation,excerpt,relevance,"
                    "adoption_status,source_document"
                ),
                (
                    "climate,climate-plan-2.4,climate,Low-carbon retrofit priority,"
                    "Climate Plan Policy C-2.4,Prioritize low-carbon retrofits in civic facilities,"
                    "Relevant when capital projects alter municipal buildings,adopted,"
                    "Climate Action Plan 2026"
                ),
            ]
        ),
        encoding="utf-8",
    )

    summary = import_local_policies(db_url=db_url, policies_csv=policies_csv)
    repository = PlanPolicyRepository(db_url=db_url, seed_defaults=False)
    policy, source = repository.lookup_policy_with_source(topic="climate retrofit", plan_type="climate")

    assert summary.policies == 1
    assert source == "persisted"
    assert policy.policy_id == "climate-plan-2.4"
    assert policy.citation == "Climate Plan Policy C-2.4"
    assert len(repository.list_policies()) == 1


def test_local_policy_import_validates_csv_before_writing(tmp_path) -> None:
    db_url = f"sqlite:///{tmp_path / 'invalid.db'}"
    policies_csv = tmp_path / "policies.csv"
    policies_csv.write_text(
        "\n".join(
            [
                "topic_key,policy_id,plan_type,title,citation,excerpt,relevance,adoption_status",
                (
                    "climate,climate-plan-2.4,climate,Low-carbon retrofit priority,"
                    "Climate Plan Policy C-2.4,Prioritize low-carbon retrofits,"
                    "Relevant to capital projects,adopted"
                ),
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing required columns: source_document"):
        import_local_policies(db_url=db_url, policies_csv=policies_csv)

    repository = PlanPolicyRepository(db_url=db_url, seed_defaults=False)
    assert repository.list_policies() == ()
