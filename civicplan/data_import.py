from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

from civicplan.persistence import PlanPolicyRepository
from civicplan.plan_workflows import normalize_ingested_policy


POLICY_COLUMNS = {
    "topic_key",
    "policy_id",
    "plan_type",
    "title",
    "citation",
    "excerpt",
    "relevance",
    "adoption_status",
    "source_document",
}


@dataclass(frozen=True)
class ImportSummary:
    policies: int = 0


def import_local_policies(*, db_url: str, policies_csv: Path) -> ImportSummary:
    """Validate and import local municipal plan-policy CSV rows into CivicPlan."""

    records = [
        normalize_ingested_policy(
            topic_key=_required(row, "topic_key"),
            policy_id=_required(row, "policy_id"),
            plan_type=_required(row, "plan_type"),
            title=_required(row, "title"),
            citation=_required(row, "citation"),
            excerpt=_required(row, "excerpt"),
            relevance=_required(row, "relevance"),
            adoption_status=_required(row, "adoption_status"),
            source_document=_required(row, "source_document"),
        )
        for row in _read_rows(policies_csv)
    ]

    repository = PlanPolicyRepository(db_url=db_url, seed_defaults=False)
    for record in records:
        repository.upsert_policy(topic_key=record.topic_key, policy=record.policy)
    return ImportSummary(policies=len(records))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Import local municipal plan-policy CSV rows into CivicPlan."
    )
    parser.add_argument(
        "--db-url",
        required=True,
        help="SQLAlchemy database URL for CivicPlan policy records.",
    )
    parser.add_argument(
        "--policies-csv",
        required=True,
        type=Path,
        help="CSV with local plan-policy rows.",
    )
    args = parser.parse_args(argv)

    summary = import_local_policies(db_url=args.db_url, policies_csv=args.policies_csv)
    print(f"CivicPlan import complete: {summary.policies} policies.")
    return 0


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing = sorted(POLICY_COLUMNS - fieldnames)
        if missing:
            raise ValueError(f"{path} is missing required columns: {', '.join(missing)}")
        rows = list(reader)
    for index, row in enumerate(rows, start=2):
        for column in POLICY_COLUMNS:
            if row.get(column, "").strip() == "":
                raise ValueError(f"{path}:{index} has an empty required value for {column}")
    return rows


def _required(row: dict[str, str], column: str) -> str:
    return row[column].strip()


if __name__ == "__main__":
    raise SystemExit(main())
