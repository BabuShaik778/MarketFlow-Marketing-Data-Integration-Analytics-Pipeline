import pytest
from etl import clean_text, normalize_status, normalize_phone, parse_date

def test_clean_text():
    assert clean_text("  hello  ") == "hello"

def test_status_normalization():
    assert normalize_status(" NEW ") == "new"

def test_phone_normalization():
    assert normalize_phone("+91 98765 43210") == "9876543210"

def test_short_phone_is_invalid():
    with pytest.raises(ValueError):
        normalize_phone("12345")

def test_date_normalization():
    assert parse_date("2026-03-01") == "2026-03-01"
