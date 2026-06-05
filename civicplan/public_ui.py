"""Public UI shell for CivicPlan v0.2.2."""

from __future__ import annotations


def render_public_lookup_page() -> str:
    """Render the public-facing CivicPlan lookup page."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CivicPlan Public Policy Lookup</title>
<style>
  :root {
    --ink:#17202a;
    --muted:#56606a;
    --surface:#fbfbf8;
    --panel:#ffffff;
    --blue:#215f88;
    --green:#2f6b50;
    --amber:#a96818;
    --red:#9a3f2d;
    --line:#cfd6da;
    --focus:#d8b45b;
  }
  * { box-sizing:border-box; }
  body {
    margin:0;
    color:var(--ink);
    font-family:"Aptos","Segoe UI",sans-serif;
    background:var(--surface);
  }
  .skip-link {
    position:absolute;
    left:1rem;
    top:-4rem;
    background:var(--ink);
    color:white;
    padding:.65rem .9rem;
    border-radius:4px;
  }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:min(1160px, calc(100% - 32px)); margin:0 auto; }
  header { padding:34px 0 18px; border-bottom:1px solid var(--line); }
  .eyebrow { color:var(--blue); text-transform:uppercase; letter-spacing:.12em; font-weight:800; font-size:.78rem; }
  h1 { max-width:980px; margin:.15rem 0 0; font-size:clamp(2.1rem,5vw,4rem); line-height:1.02; letter-spacing:0; }
  .lede { max-width:850px; font-size:1.08rem; line-height:1.55; color:#31404a; }
  .badge { display:inline-flex; width:fit-content; padding:.4rem .65rem; border-radius:4px; background:var(--green); color:white; font-weight:800; }
  main { padding:22px 0 8px; }
  .grid { display:grid; grid-template-columns:repeat(12,1fr); gap:14px; align-items:start; }
  .panel {
    grid-column:span 6;
    min-width:0;
    padding:18px;
    border:1px solid var(--line);
    border-radius:8px;
    background:var(--panel);
  }
  .panel.large { grid-column:span 12; }
  h2,h3 { margin:0; letter-spacing:0; }
  h2 { font-size:1.45rem; }
  h3 { font-size:1.05rem; }
  p, li { line-height:1.55; }
  label { display:block; margin:.8rem 0 .35rem; font-weight:800; }
  input, textarea, select {
    width:100%;
    border:1px solid #aeb8bf;
    border-radius:6px;
    padding:.72rem .78rem;
    color:var(--ink);
    background:white;
    font:inherit;
  }
  textarea { min-height:90px; resize:vertical; }
  .row { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
  .actions { display:flex; flex-wrap:wrap; gap:10px; margin-top:14px; }
  button {
    border:0;
    border-radius:6px;
    padding:.74rem .95rem;
    background:var(--blue);
    color:white;
    font-weight:850;
    cursor:pointer;
  }
  button.secondary { background:var(--green); }
  button:disabled { cursor:not-allowed; opacity:.65; }
  .kicker { color:var(--muted); font-size:.78rem; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
  .result {
    margin-top:16px;
    padding:14px;
    border-left:5px solid var(--green);
    border-radius:6px;
    background:#f7fbf9;
  }
  .result.pending { border-left-color:var(--amber); background:#fffaf2; }
  .result.error { border-left-color:var(--red); background:#fff6f4; }
  .result ul { padding-left:1.2rem; margin-bottom:0; }
  .policy-list { display:grid; gap:10px; margin-top:12px; }
  .policy-item { border:1px solid var(--line); border-radius:6px; padding:12px; background:#fbfcfd; }
  .notice { margin:18px 0 0; padding:16px; border:1px dashed var(--red); border-radius:8px; background:#fff8f4; }
  footer { padding:28px 0 48px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--focus); outline-offset:2px; }
  @media (max-width:760px) {
    header,main,footer { width:100%; padding-left:18px; padding-right:18px; }
    header { padding-top:28px; }
    h1 { font-size:2.25rem; }
    .panel { grid-column:span 12; padding:16px; }
    .row { grid-template-columns:1fr; }
    button { width:100%; }
  }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicPlan</p>
  <h1>Find cited plan policies before the meeting packet gets written.</h1>
  <p class="lede">CivicPlan lets staff and residents look up adopted policy context, ask cited planning questions, and prepare review-required consistency support without turning software into the decision-maker.</p>
  <p><span class="badge">v0.2.2 cited plan policy + staff analysis</span></p>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-label="CivicPlan lookup tools">
    <article class="panel large">
      <p class="kicker">Plan-policy lookup</p>
      <h2>Search local plan policy context</h2>
      <form id="lookup-form">
        <div class="row">
          <div>
            <label for="topic">Topic or proposal</label>
            <textarea id="topic" name="topic">A small mixed-use housing project near transit, a school, and a neighborhood park.</textarea>
          </div>
          <div>
            <label for="plan-type">Plan type</label>
            <select id="plan-type" name="plan_type">
              <option value="comprehensive">Comprehensive plan</option>
              <option value="transportation">Transportation plan</option>
              <option value="parks">Parks plan</option>
            </select>
            <label for="question">Question</label>
            <input id="question" name="question" value="What does the plan say about missing middle housing near services?">
          </div>
        </div>
        <div class="actions">
          <button type="submit">Look Up Policy</button>
          <button class="secondary" type="button" id="ask-button">Ask Cited Question</button>
        </div>
      </form>
      <div id="lookup-result" class="result pending" role="status" aria-live="polite">
        Enter a topic or question to retrieve cited plan context from the local CivicPlan API.
      </div>
    </article>
    <article class="panel">
      <p class="kicker">Consistency support</p>
      <h2>Support, not determination</h2>
      <form id="consistency-form">
        <label for="proposal">Proposal summary</label>
        <textarea id="proposal" name="proposal">Mixed-use housing near transit, sidewalks, and a neighborhood park.</textarea>
        <label for="policy-id">Policy ID</label>
        <input id="policy-id" name="policy_id" value="housing">
        <div class="actions"><button type="submit">Check Consistency Support</button></div>
      </form>
      <div id="consistency-result" class="result pending" role="status" aria-live="polite">
        Results remain planning support. Staff must make official findings.
      </div>
    </article>
    <article class="panel">
      <p class="kicker">Plan navigator</p>
      <h2>Browse cited structure</h2>
      <div class="actions"><button type="button" id="navigator-button">Load Plans</button></div>
      <div id="navigator-result" class="result pending" role="status" aria-live="polite">
        Load available local plan policies grouped by plan type.
      </div>
    </article>
    <article class="panel">
      <p class="kicker">Progress tracking</p>
      <h2>Evidence, not findings</h2>
      <div class="actions"><button type="button" id="progress-button">Load Targets</button></div>
      <div id="progress-result" class="result pending" role="status" aria-live="polite">
        Load progress target evidence and review-required boundaries.
      </div>
    </article>
    <article class="panel">
      <p class="kicker">Records-ready export</p>
      <h2>Keep provenance</h2>
      <div class="result"><p>Exports preserve source policy, proposal text, reviewer, generated outline, and final staff edits for the municipal record.</p></div>
    </article>
    <article class="panel">
      <p class="kicker">Planning boundary</p>
      <h2>No official determination</h2>
      <div class="result error"><p>CivicPlan does not make zoning, land-use, environmental, legal, or elected-body decisions. Staff and officials remain responsible for every official action.</p></div>
    </article>
  </section>
  <section class="notice" aria-labelledby="boundary-title">
    <h2 id="boundary-title">Important boundaries</h2>
    <p>CivicPlan v0.2.2 is a corrective demotion release that supersedes the false v1.0.0 release from 2026-05-21 in GitHub's Latest impression. The CivicCore pin is aligned to the current city-core platform. CivicPlan provides cited plan lookup, local policy ingestion when configured, CivicZone and CivicClerk context contracts, amendment history, progress targets, and adversarial local integration validation. It does not call live external systems by default, provide legal advice, or make official planning determinations.</p>
  </section>
</main>
<footer><p>CivicPlan is part of the Apache 2.0 CivicSuite open-source municipal AI project.</p></footer>
<script>
const endpoints = {
  lookup: "/api/v1/civicplan/policies/lookup",
  question: "/api/v1/civicplan/questions/answer",
  consistency: "/api/v1/civicplan/consistency/check",
  navigator: "/api/v1/civicplan/plans/navigator",
  progress: "/api/v1/civicplan/progress/targets"
};

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => {
    if (char === "&") return "&amp;";
    if (char === "<") return "&lt;";
    if (char === ">") return "&gt;";
    if (char === '"') return "&quot;";
    return "&#39;";
  });
}

function setPending(target, message) {
  target.className = "result pending";
  target.innerHTML = escapeHtml(message);
}

function setError(target, error) {
  const detail = error?.detail;
  const message = detail?.message || error?.message || "CivicPlan could not complete the request.";
  const fix = detail?.fix ? `<p><strong>Fix:</strong> ${escapeHtml(detail.fix)}</p>` : "";
  target.className = "result error";
  target.innerHTML = `<h3>Needs attention</h3><p>${escapeHtml(message)}</p>${fix}`;
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: {"Content-Type": "application/json"},
    ...options
  });
  const payload = await response.json();
  if (!response.ok) {
    throw payload;
  }
  return payload;
}

function renderPolicy(policy) {
  return `
    <h3>${escapeHtml(policy.title || policy.policy_id)}</h3>
    <p><strong>${escapeHtml(policy.citation)}</strong></p>
    <p>${escapeHtml(policy.excerpt)}</p>
    <p><strong>Relevance:</strong> ${escapeHtml(policy.relevance)}</p>
    <p><strong>Boundary:</strong> ${escapeHtml(policy.disclaimer)}</p>
  `;
}

document.getElementById("lookup-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const target = document.getElementById("lookup-result");
  setPending(target, "Looking up cited plan policy...");
  try {
    const payload = await requestJson(endpoints.lookup, {
      method: "POST",
      body: JSON.stringify({
        topic: document.getElementById("topic").value,
        plan_type: document.getElementById("plan-type").value
      })
    });
    target.className = "result";
    target.innerHTML = renderPolicy(payload);
  } catch (error) {
    setError(target, error);
  }
});

document.getElementById("ask-button").addEventListener("click", async () => {
  const target = document.getElementById("lookup-result");
  setPending(target, "Answering with cited plan context...");
  try {
    const payload = await requestJson(endpoints.question, {
      method: "POST",
      body: JSON.stringify({
        question: document.getElementById("question").value,
        plan_type: document.getElementById("plan-type").value
      })
    });
    target.className = "result";
    target.innerHTML = `
      <h3>Cited Answer</h3>
      <p>${escapeHtml(payload.answer)}</p>
      <p><strong>Citations:</strong> ${escapeHtml(payload.citations.join("; "))}</p>
      <p><strong>Review required:</strong> ${payload.review_required ? "Yes" : "No"}</p>
      <p>${escapeHtml(payload.disclaimer)}</p>
    `;
  } catch (error) {
    setError(target, error);
  }
});

document.getElementById("consistency-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const target = document.getElementById("consistency-result");
  setPending(target, "Checking consistency support...");
  try {
    const payload = await requestJson(endpoints.consistency, {
      method: "POST",
      body: JSON.stringify({
        proposal: document.getElementById("proposal").value,
        policy_id: document.getElementById("policy-id").value
      })
    });
    target.className = "result";
    target.innerHTML = `
      <h3>${escapeHtml(payload.status)}</h3>
      <ul>${payload.factors.map((factor) => `<li>${escapeHtml(factor)}</li>`).join("")}</ul>
      <p><strong>Next step:</strong> ${escapeHtml(payload.staff_next_step)}</p>
      <p>${escapeHtml(payload.disclaimer)}</p>
    `;
  } catch (error) {
    setError(target, error);
  }
});

document.getElementById("navigator-button").addEventListener("click", async () => {
  const target = document.getElementById("navigator-result");
  setPending(target, "Loading plan navigator...");
  try {
    const payload = await requestJson(endpoints.navigator);
    target.className = "result";
    target.innerHTML = `
      <h3>Plan Policies</h3>
      <div class="policy-list">
        ${payload.plans.map((plan) => `
          <div class="policy-item">
            <strong>${escapeHtml(plan.plan_type)}</strong>
            <ul>${plan.policies.map((policy) => `<li>${escapeHtml(policy.policy_id)}: ${escapeHtml(policy.citation)}</li>`).join("")}</ul>
          </div>
        `).join("")}
      </div>
      <p>${escapeHtml(payload.boundary)}</p>
    `;
  } catch (error) {
    setError(target, error);
  }
});

document.getElementById("progress-button").addEventListener("click", async () => {
  const target = document.getElementById("progress-result");
  setPending(target, "Loading progress targets...");
  try {
    const payload = await requestJson(endpoints.progress);
    target.className = "result";
    target.innerHTML = `
      <h3>Progress Targets</h3>
      <ul>${payload.items.map((item) => `<li><strong>${escapeHtml(item.policy_id)}</strong>: ${escapeHtml(item.status)}. ${escapeHtml(item.evidence)}</li>`).join("")}</ul>
      <p>${escapeHtml(payload.boundary)}</p>
    `;
  } catch (error) {
    setError(target, error);
  }
});
</script>
</body>
</html>
"""
