"""Smoke test for the validator facade."""

from validate_phyphox import validate_phyphox

pytest_plugins = ("tests.test_phyphox_validation_contracts",)


class TestValidFile:
    def test_minimal_valid_passes(self, valid_phyphox_file):
        errors = validate_phyphox(valid_phyphox_file)
        assert errors == []
