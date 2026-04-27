"""FastAPI runtime foundation for CivicPlan."""

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicplan import __version__
from civicplan.consistency import check_policy_consistency
from civicplan.policy_lookup import lookup_plan_policy
from civicplan.public_ui import render_public_lookup_page
from civicplan.records_export import build_policy_export
from civicplan.staff_analysis import draft_staff_analysis


app = FastAPI(
    title="CivicPlan",
    version=__version__,
    description="Comprehensive-plan policy lookup and cited planning analysis support for CivicSuite.",
)


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
        "status": "planning policy foundation",
        "message": (
            "CivicPlan package, API foundation, sample cited plan-policy lookup, policy-consistency support, staff-analysis outline, records-ready export checklist, and public UI foundation are online; "
            "official planning determinations, live GIS, live LLM calls, plan document ingestion, and permitting-system integrations are not implemented yet."
        ),
        "next_step": "Post-v0.1.0 roadmap: plan ingestion, CivicZone policy context API, and staff review workflows",
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
    result = lookup_plan_policy(topic=request.topic, plan_type=request.plan_type)
    return result.__dict__


@app.post("/api/v1/civicplan/consistency/check")
def consistency_check(request: ConsistencyRequest) -> dict[str, object]:
    result = check_policy_consistency(proposal=request.proposal, policy_id=request.policy_id)
    return result.__dict__


@app.post("/api/v1/civicplan/staff-analysis/draft")
def staff_analysis(request: StaffAnalysisRequest) -> dict[str, object]:
    result = draft_staff_analysis(
        project_name=request.project_name,
        proposal=request.proposal,
        policy_id=request.policy_id,
    )
    return result.__dict__


@app.post("/api/v1/civicplan/export")
def policy_export(request: PolicyExportRequest) -> dict[str, object]:
    result = build_policy_export(title=request.title, policy_id=request.policy_id, format=request.format)
    return result.__dict__
