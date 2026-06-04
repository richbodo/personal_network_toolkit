# Architecture (dirty fixture)

Three `conformant` rows with bad evidence. The lint must exit 1 and name each.

### AC attestation table

| AC | Realization | Verification | Status |
|---|---|---|---|
| AC-1 (ok) | Enforced and asserted. | `tests/test_sample.py::test_real_invariant` | conformant |
| AC-2 (xfail as evidence) | Claimed enforced. | `tests/test_sample.py::test_deferred` | conformant |
| AC-3 (doc-only) | Asserted in the design notes. | see design-notes.md | conformant |
| AC-4 (dangling) | Claimed covered. | `tests/test_missing.py::test_nope` | conformant |
