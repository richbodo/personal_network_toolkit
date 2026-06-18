# AC-PRM-H — authenticated loopback surface · field notes

*Surfaced by [prm #59](https://github.com/richbodo/prm/pull/59) (daemon session-auth + the loopback-surface lint). The AC: [`spec/axes.md` § Workspace shell](../../spec/axes.md#ac-prm-h).*

## Lesson

A PNA that serves its workspace over a **local HTTP daemon** has widened its own
attack surface beyond the OS file-permission baseline: a sandboxed / lower-priv /
network-only process that *cannot read the store file* can still `curl`
`127.0.0.1` and read everything if the daemon is unauthenticated. The app opened
this surface, so the app must close it — **loopback-bind *and* authenticate to the
user's own session.** This is *intrinsic* (the app can close it), not an
environmental (Harden) concern — the test that sorts the two.

## Negative invariants (what a candidate is easy to pass by accident)

- **A non-loopback bind must not exist without an explicit, documented opt-out.**
  `0.0.0.0` / `""` / a public host exposes the surface off-device. Pinned by the
  loopback lint's **L1** (gates) + PRM's loopback-pin test (a non-`--host` daemon
  refuses to bind a public interface) in `tests/unit/test_daemon_security.py`.
- **An unauthenticated `/api/*` must not return Private data to another local
  process.** Pin it with a *negative* test — request without the session token →
  `401` (PRM: `test_daemon_security.py`). The happy-path "works with the token"
  test does **not** cover this.
- **Authenticating the transport must NOT flip `pna-active`.** It relaxes no
  guarantee (data stays on-device; the app talks only to itself), so over-flagging
  it would dilute the one bit a relying party keys on.

## Pitfalls / look hardest at

- **The auth-guard heuristic is fuzzy.** `tools/loopback-surface-lint.py` **L2**
  flags the *absence* of a recognized guard; it can neither prove a present guard
  is *sufficient* nor that an unrecognized one is missing. That's why L2 is
  **advisory** by default (`--strict` to gate). Confirm enforcement with the
  design's negative tests, never with the lint alone. (`just loopback-lint <dir>`.)
- **You can't identify the caller.** Like the MCP boundary, the daemon can't tell
  *which* local process is dialing — so the boundary is held by **authentication +
  honest signaling**, never by trying to identify the client.
- **Auth does not stop a same-UID agent** that can read the session token from the
  page/process or drive the real UI. That residue is **Surface 3** (Harden flow),
  not this AC — don't credit the loopback auth with closing it.

## Surfaced by

PRM [#59](https://github.com/richbodo/prm/pull/59) (merged; durable at `main` @
`1551896`) — daemon session-auth (token + Host/Origin guard + loopback-pin) + the
L1/L2 loopback lint run `--strict` in its conformance gate. Realized as `AC-2`'s
intent generalized to the app's own local transport (the "no ungoverned data tap"
principle under [`spec/axes.md` § Distribution](../../spec/axes.md#distribution)).
