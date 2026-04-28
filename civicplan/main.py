"""FastAPI runtime foundation for CivicPlan."""

import os

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicplan import __version__
from civicplan.consistency import check_policy_consistency
from civicplan.persistence import PlanPolicyRepository, StoredStaffAnalysis
from civicplan.policy_lookup import lookup_plan_policy
from civicplan.public_ui import render_public_lookup_page
from civicplan.records_export import build_policy_export
from civicplan.staff_analysis import draft_staff_analysis


app = FastAPI(
    title="CivicPlan",
    version=__version__,
    description="Comprehensive-plan policy lookup and cited planning analysis support for CivicSuite.",
)

_policy_repository: PlanPolicyRepository | None = None
_policy_db_url: str | None = None


class PolicyLookupRequest(BaseModel):
    topic: str
    plan_type: str = "comprehensive"


class ConsistencyRequest(BaseModel):
    proposal: str
    policy_id: str


class StaffAnalysisRequest(BaseModel):
    project_name: str
    proposal: str
    policy_id: str


class PolicyExportRequest(BaseModel):
    title: str
    policy_id: str
    format: str = "markdown"


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicPlan",
        "version": __version__,
        "status": "planning policy foundation plus policy persistence",
        "message": (
            "CivicPlan package, API foundation, sample cited plan-policy lookup, optional database-backed policy and staff-analysis records, policy-consistency support, staff-analysis outline, records-ready export checklist, and public UI foundation are online; "
            "official planning determinations, live GIS, live LLM calls, plan document ingestion, and permitting-system integrations are not implemented yet."
        ),
        "next_step": "Post-v0.1.1 roadmap: plan ingestion, CivicZone policy context API, and staff review workflows",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return dependency/version health for deployment smoke checks."""

    return {
        "status": "ok",
        "service": "civicplan",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civicplan", response_class=HTMLResponse)
def public_civicplan_page() -> str:
    """Return the public sample plan-policy lookup UI."""

    return render_public_lookup_page()


@app.post("/api/v1/civicplan/policies/lookup")
def policy_lookup(request: PolicyLookupRequest) -> dict[str, object]:
    result = _lookup_plan_policy(topic=request.topic, plan_type=request.plan_type)
    return result.__dict__


@app.post("/api/v1/civicplan/consistency/check")
def consistency_check(request: ConsistencyRequest) -> dict[str, object]:
    result = check_policy_consistency(proposal=request.proposal, policy_id=request.policy_id)
    return result.__dict__


@app.post("/api/v1/civicplan/staff-analysis/draft")
def staff_analysis(request: StaffAnalysisRequest) -> dict[str, object]:
    if _policy_database_url() is not None:
        stored = _get_policy_repository().create_staff_analysis(
            project_name=request.project_name,
            proposal=request.proposal,
            policy_id=request.policy_id,
        )
        return _stored_staff_analysis_response(stored)

    result = draft_staff_analysis(
        project_name=request.project_name,
        proposal=request.proposal,
        policy_id=request.policy_id,
    )
    payload = result.__dict__
    payload["analysis_id"] = None
    return payload


@app.get("/api/v1/civicplan/staff-analysis/{analysis_id}")
def get_staff_analysis(analysis_id: str) -> dict[str, object]:
    if _policy_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "CivicPlan policy persistence is not configured.",
                "fix": "Set CIVICPLAN_POLICY_DB_URL to retrieve persisted staff-analysis records.",
            },
        )
    stored = _get_policy_repository().get_staff_analysis(analysis_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Staff-analysis record not found.",
                "fix": "Use an analysis_id returned by POST /api/v1/civicplan/staff-analysis/draft.",
            },
        )
    return _stored_staff_analysis_response(stored)


@app.post("/api/v1/civicplan/export")
def policy_export(request: PolicyExportRequest) -> dict[str, object]:
    result = build_policy_export(title=request.title, policy_id=request.policy_id, format=request.format)
    return result.__dict__


def _policy_database_url() -> str | None:
    return os.environ.get("CIVICPLAN_POLICY_DB_URL")


def _get_policy_repository() -> PlanPolicyRepository:
    global _policy_db_url, _policy_repository
    db_url = _policy_database_url()
    if db_url is None:
        raise RuntimeError("CIVICPLAN_POLICY_DB_URL is not configured.")
    if _policy_repository is None or db_url != _policy_db_url:
        _dispose_policy_repository()
        _policy_db_url = db_url
        _policy_repository = PlanPolicyRepository(db_url=db_url)
    return _policy_repository


def _dispose_policy_repository() -> None:
    global _policy_repository
    if _policy_repository is not None:
        _policy_repository.engine.dispose()
        _policy_repository = None


def _lookup_plan_policy(*, topic: str, plan_type: str = "comprehensive"):
    if _policy_database_url() is None:
        return lookup_plan_policy(topic=topic, plan_type=plan_type)
    return _get_policy_repository().lookup_policy(topic=topic, plan_type=plan_type)


def _stored_staff_analysis_response(stored: StoredStaffAnalysis) -> dict[str, object]:
    return {
        "analysis_id": stored.analysis_id,
        "project_name": stored.project_name,
        "proposal": stored.proposal,
        "policy_id": stored.policy_id,
        "heading": stored.heading,
        "bullets": list(stored.bullets),
        "citations": list(stored.citations),
        "review_required": stored.review_required,
        "disclaimer": stored.disclaimer,
        "created_at": stored.created_at.isoformat(),
    }
