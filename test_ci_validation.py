"""Temporary test used to confirm that CI detects pytest failures."""


def test_ci_detects_incorrect_expectation():
    """Intentionally fail so the CI test stage can be verified."""
    assert 200 == 201
