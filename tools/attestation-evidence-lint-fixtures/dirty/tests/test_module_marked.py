"""Dirty-fixture: every test here is deferred via a module-level `pytestmark`
global rather than a per-def decorator. A `conformant` row citing one of these
is the same false-evidence bug as a decorated xfail, just hoisted one scope up —
the lint must catch it all the same."""
import pytest

pytestmark = pytest.mark.xfail(strict=True, reason="deferred; not yet enforced. tracking: #3")


def test_hoisted():
    assert False
