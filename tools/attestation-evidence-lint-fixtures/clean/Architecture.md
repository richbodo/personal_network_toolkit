# Architecture (clean fixture)

A minimal AC attestation table where every `conformant` row carries live
evidence. The lint must exit 0 against this design root.

### AC attestation table

| AC | Realization | Verification | Status |
|---|---|---|---|
| AC-1 (real test) | The invariant is enforced and asserted directly. | `tests/test_sample.py::test_real_invariant` | conformant |
| AC-2 (env-guarded test) | Asserted by a test guarded on a platform precondition; runs in CI. | `tests/test_sample.py::test_guarded` | conformant |
| AC-3 (review kind) | Holds structurally; no test, an explicitly declared kind. | by construction | conformant |
| AC-4 (file-level ref) | Covered across the file's cases. | `tests/test_sample.py` | conformant |
| AC-5 (honest deferral) | Designed but not yet enforced. | `tests/test_sample.py::test_deferred` (xfail) | partial-conformance (Open) |
| AC-6 (honest non-conformance) | Known gap; not yet enforced. | (none — fix pending) | non-conformant |
