# PNA Toolkit — command runner. Run `just` with no args for the menu.
#
# This is a spec/lint/docs toolkit: every recipe wraps a stdlib-only python3 tool
# or shell script, so there is no setup/venv step — python3 (3.10+) is the only
# requirement. Recipe names mirror the underlying tools deliberately.
#
# Examples:
#   just ci                                              # the full gate before pushing
#   just egress-lint ../candidate --json                 # AC-1 egress scan of a candidate PNA
#   just export-lint ../candidate/export                 # PR-6 export-readability check
#   just swh-save https://github.com/you/your-pna v1.0   # archive + print SWHID fields

set shell := ["bash", "-euo", "pipefail", "-c"]

python := "python3"
venv := ".venv"

# Show the recipe menu.
default:
    @just --list


# ---- check ---------------------------------------------------------------

# Lint + self-tests — the full CI gate (run before pushing).
[group('check')]
ci: lint lint-selftest

# Spec / contract / version / constraint / manifest lint (tools/lint-spec-ids.py).
[group('check')]
lint:
    {{python}} tools/lint-spec-ids.py

# Toolkit self-tests — assert the lints fail on injected faults (tools/tests/lint_selftest.py).
[group('check')]
lint-selftest:
    {{python}} tools/tests/lint_selftest.py


# ---- evaluate ------------------------------------------------------------

# Egress-scan a candidate PNA dir for off-device vectors, AC-1 (args pass through).
[group('evaluate')]
egress-lint target *args:
    {{python}} tools/egress-lint.py {{target}} {{args}}

# Check a Private-DB export is tool-free readable, PR-6 (args pass through).
[group('evaluate')]
export-lint target *args:
    {{python}} tools/export-readable-lint.py {{target}} {{args}}

# Check a design's `conformant` attestation rows cite live, non-deferred evidence (args pass through).
[group('evaluate')]
attestation-lint target *args:
    {{python}} tools/attestation-evidence-lint.py {{target}} {{args}}

# Validate evaluate-report.json instance(s) against the render contract (Visual Validator input).
[group('evaluate')]
report-lint target:
    {{python}} tools/report-fixtures-lint.py {{target}}


# ---- design --------------------------------------------------------------

# Software Heritage archival + print paste-ready design.toml SWHID fields. Args: <repo-url> [ref] [clone].
[group('design')]
swh-save url ref="HEAD" clone="":
    tools/swh-save.sh {{url}} {{ref}} {{clone}}

# (Scaffold, Phase 4) fetch -> verify SWHID -> build -> run a design's [verify] entrypoint; inert for now.
[group('design')]
test-design name:
    @echo "Phase 4 is not active yet: this would fetch reference design '{{name}}',"
    @echo "verify 'git rev-parse HEAD^{tree} == swhid_dir', build it, and run its"
    @echo "[verify] entrypoint. See plans/conformance-suite-plan.md § Phase 4."
    @exit 1


# ---- browser-test (opt-in; NOT part of `just ci`) ------------------------

# One-time: create .venv + install the opt-in browser-test deps (pytest + Playwright + chromium).
[group('browser-test')]
setup-test:
    {{python}} -m venv {{venv}}
    {{venv}}/bin/pip install --quiet --upgrade pip
    {{venv}}/bin/pip install --quiet -r requirements-dev.txt
    {{venv}}/bin/playwright install chromium

# Render-test the Visual Validator viewer in a real browser (opt-in; NOT in `just ci`; run `just setup-test` first).
[group('browser-test')]
test-viewer *args:
    {{venv}}/bin/pytest tools/report-viewer/tests/ {{args}}
