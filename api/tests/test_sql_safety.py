import pytest
from sql_safety import validate_sql_is_safe, enforce_row_limit


def test_valid_select_passes():
    validate_sql_is_safe("SELECT * FROM customers")


def test_non_select_rejected():
    with pytest.raises(ValueError):
        validate_sql_is_safe("DELETE FROM customers")


def test_forbidden_keyword_rejected():
    with pytest.raises(ValueError):
        validate_sql_is_safe("SELECT * FROM customers; DROP TABLE customers")


def test_statement_chaining_rejected():
    with pytest.raises(ValueError):
        validate_sql_is_safe("SELECT 1; SELECT 2")


def test_limit_auto_appended():
    result = enforce_row_limit("SELECT * FROM customers")
    assert "LIMIT" in result.upper()


def test_existing_limit_not_duplicated():
    result = enforce_row_limit("SELECT * FROM customers LIMIT 5")
    assert result.upper().count("LIMIT") == 1