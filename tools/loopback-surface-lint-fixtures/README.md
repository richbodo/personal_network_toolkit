# loopback-surface-lint fixtures

Inputs for `tools/loopback-surface-lint.py` and its self-tests in
`tools/tests/lint_selftest.py`. The lint flags the one surface a PNA opens over
its *own* data (an app-stood-up HTTP daemon — candidate `AC-PRM-H`, RFC; the design note
and the AC itself land with their demonstrator, PRM), at two severities:

| Dir | What it is | Default exit | `--strict` exit |
|---|---|---|---|
| `clean/`  | loopback bind (a variable, default `127.0.0.1`) + a constant-time token check + Host allowlist | `0` (no findings) | `0` |
| `dirty/`  | **L1** — server bound to a literal `0.0.0.0` (every interface, off-device) | `1` (gates) | `1` |
| `noauth/` | **L2** — loopback-bound, but the handler shows *no* auth guard | `0` (advisory only) | `1` (promoted) |

**Why the split.** `L1` (a literal non-loopback bind) is unambiguous, so it gates.
`L2` (absence of any recognized auth signal in a handler module) is a *heuristic* —
it can't prove an unrecognized guard is missing — so it is **advisory** by default,
to keep a heuristic from rotting into alarm-fatigued CI noise. A design that knows
its own auth shape opts into `L2`-as-gate for itself with `--strict`. This is the
same bounded-claim posture as `egress-lint`: a tripwire, not a proof of enforcement.
