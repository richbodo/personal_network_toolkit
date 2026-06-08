# report-fixtures-lint fixtures

Self-test inputs for [`../report-fixtures-lint.py`](../report-fixtures-lint.py).

- **Clean inputs are the real samples** at [`../report-viewer/sample-reports/`](../report-viewer/sample-reports/)
  — the self-test runs the lint against that directory and expects **exit 0**, so the Visual Validator's
  actual render fixtures are continuously validated (no duplicated clean copy to drift).
- **`dirty/`** — a deliberately broken report (`conformant-without-citations.json`: a `conformant`
  finding with no `citations`, violating the schema's status-conditional rule). Expected: **exit 1**.

The self-test wiring is in [`../tests/lint_selftest.py`](../tests/lint_selftest.py) via `case_fixture_lint`
(clean dir passes; dirty dir fails), matching the egress / export / attestation lints.
