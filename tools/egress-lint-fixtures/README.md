# egress-lint fixtures

Self-test inputs for [`../egress-lint.py`](../egress-lint.py). PNT bundles no
application code, so these fixtures are how PNT's own CI exercises the lint (the
real target of the lint is a reference design's source tree, in that design's
repo).

- **`clean/`** — every egress vector is local or allow-listed (`egress-allow.json`
  sanctions the single remote origin the flavor needs). Expected: **exit 0**.
  Also a regression guard against false positives (`xmlns`, `<a href>`,
  `mailto:`, `data:`, localhost, root-relative paths must NOT be flagged).
- **`dirty/`** — unsanctioned egress to non-allow-listed remote origins, no
  allow-list. Expected: **exit 1** with one violation per off-device vector.

CI (`.github/workflows/spec-lint.yml`) runs both and asserts the exit codes.
