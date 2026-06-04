"""Clean-fixture test file for attestation-evidence-lint self-tests."""
import sys

import pytest


def test_real_invariant():
    assert True


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX-only path semantics")
def test_guarded():
    # A conditional skipif is a legitimate environment guard — it runs in CI on
    # the supported platforms. The lint must NOT treat it as disqualifying.
    assert True


@pytest.mark.xfail(strict=True, reason="deferred; off-folder gating. tracking: #1")
def test_deferred():
    # Cited only by an honest `partial`/Open row, which the lint exempts.
    assert False
