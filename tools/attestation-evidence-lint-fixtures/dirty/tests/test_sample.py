"""Dirty-fixture test file for attestation-evidence-lint self-tests."""
import pytest


def test_real_invariant():
    assert True


@pytest.mark.xfail(strict=True, reason="deferred; not yet enforced. tracking: #2")
def test_deferred():
    # Cited by a `conformant` row in this fixture's Architecture.md — that is the
    # bug the lint exists to catch: a declared-false invariant as evidence.
    assert False
