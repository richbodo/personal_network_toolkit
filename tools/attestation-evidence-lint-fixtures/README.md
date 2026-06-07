# attestation-evidence-lint fixtures

Self-test inputs for `tools/attestation-evidence-lint.py` (wired into
`tools/tests/lint_selftest.py`). The PNA Toolkit hosts no application code, so the lint is
exercised here against two tiny fake design roots instead of a real repo.

- **`clean/`** — every `conformant` row cites a live, non-deferred test or a
  declared review kind. Run against it the lint exits **0**. It deliberately
  includes the cases that must *not* trip the lint: a conditional `skipif`
  environment guard (legitimate evidence), a file-only ref, a `by construction`
  review kind, and an honest `partial` row whose evidence is an `xfail`
  (exempt — partial rows are allowed to be aspirational).
- **`dirty/`** — three textbook failures the lint must catch: a `conformant`
  row citing an `xfail(strict=True)` test (declared-false), a `conformant` row
  whose only evidence is a `.md` pointer (doc-only), and a `conformant` row
  citing a test file that doesn't exist (dangling). Run against it the lint
  exits **1**.
