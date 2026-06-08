"""Browser-render tests for the Visual Validator viewer (Playwright).

OPT-IN / not in `just ci`. Run:  just test-viewer   (one-time:  just setup-test)

These close the Phase-2 gap: they confirm the viewer actually *renders* a report
(not just that the JSON is valid — that's tools/report-fixtures-lint.py). A broken
selector or a render regression turns them red.
"""
from __future__ import annotations

import re

import pytest
from playwright.sync_api import Page, expect

# (sample file, expected posture, expected finding-card count, an ac_id that must render)
SAMPLES = [
    ("01-conformant-minimal-pna.json", "conformant", 7, "AC-MCP-A"),
    ("02-non-conformant-leaky-app.json", "non-conformant", 3, "AC-PRM-A"),
    ("03-mixed-exceptions-and-constraints.json", "mixed", 3, "AC-MCP-A"),
]


def _attach_error_capture(page: Page) -> list[str]:
    """Collect uncaught JS errors + console errors (ignoring the favicon 404 noise)."""
    errs: list[str] = []

    def on_console(msg):
        if msg.type == "error" and "favicon" not in msg.text.lower():
            errs.append("console: " + msg.text)

    page.on("console", on_console)
    page.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
    return errs


@pytest.mark.parametrize("sample,posture,n_findings,ac_id", SAMPLES)
def test_sample_renders(page: Page, viewer_url, sample, posture, n_findings, ac_id):
    errs = _attach_error_capture(page)
    page.goto(f"{viewer_url}/index.html?report=sample-reports/{sample}", wait_until="networkidle")
    page.locator(".finding").first.wait_for(state="visible", timeout=5000)

    # posture badge = first badge in the summary card (2nd .card: header, then summary)
    expect(page.locator(".card").nth(1).locator(".badge").first).to_have_text(posture)

    # findings: the right number, including a known ac_id
    ac_texts = page.locator(".finding .ac").all_inner_texts()
    assert len(ac_texts) == n_findings, f"{sample}: {len(ac_texts)} findings, expected {n_findings} ({ac_texts})"
    assert ac_id in ac_texts, f"{sample}: missing a finding for {ac_id} in {ac_texts}"

    # candidate name flows into the document title
    expect(page).to_have_title(re.compile(r" — PNA evaluate-report$"))

    assert not errs, f"{sample}: console/page errors: {errs}"


def test_evidence_source_badges_render(page: Page, viewer_url):
    """Sample 03 carries deterministic + llm + human evidence — all three badges must show."""
    page.goto(
        f"{viewer_url}/index.html?report=sample-reports/03-mixed-exceptions-and-constraints.json",
        wait_until="networkidle",
    )
    page.locator(".finding").first.wait_for(state="visible", timeout=5000)
    badges = " ".join(page.locator(".ev-src").all_inner_texts())
    for source in ("deterministic", "llm", "human"):
        assert source in badges, f"missing evidence-source badge {source!r} in {badges!r}"


def test_empty_state(page: Page, viewer_url):
    page.goto(f"{viewer_url}/index.html", wait_until="networkidle")
    expect(page.locator(".empty")).to_be_visible()


def test_malformed_report_shows_error(page: Page, viewer_url):
    page.goto(f"{viewer_url}/index.html?report=tests/fixtures/broken.json", wait_until="networkidle")
    expect(page.locator(".error")).to_be_visible()
