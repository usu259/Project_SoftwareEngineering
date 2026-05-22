import pytest
from app.domain.validations import (
    _validate_name,
    _validate_email,
    _validate_phone,
    _validate_street,
    _validate_city,
    _validate_zip_code,
    _validate_country,
    validate_text_field,
)
from app.domain.exceptions import InvalidAttributeValueError


# --- _validate_name ---

def test_validate_name_accepts_simple_name():
    assert _validate_name("Mario", "first_name") == "Mario"


def test_validate_name_strips_whitespace():
    assert _validate_name("  Mario  ", "first_name") == "Mario"


def test_validate_name_accepts_unicode():
    assert _validate_name("Müller", "last_name") == "Müller"


def test_validate_name_accepts_apostrophe():
    assert _validate_name("O'Brien", "last_name") == "O'Brien"


def test_validate_name_accepts_hyphen():
    assert _validate_name("Jean-Pierre", "first_name") == "Jean-Pierre"


def test_validate_name_rejects_empty():
    with pytest.raises(ValueError, match="first_name"):
        _validate_name("", "first_name")


def test_validate_name_rejects_digits():
    with pytest.raises(ValueError):
        _validate_name("Mar1o", "first_name")


def test_validate_name_rejects_non_string():
    with pytest.raises(TypeError):
        _validate_name(123, "first_name")


# --- _validate_email ---

def test_validate_email_accepts_valid():
    assert _validate_email("user@example.com") == "user@example.com"


def test_validate_email_strips_whitespace():
    assert _validate_email("  user@example.com  ") == "user@example.com"


def test_validate_email_rejects_no_at():
    with pytest.raises(ValueError):
        _validate_email("userexample.com")


def test_validate_email_rejects_no_dot():
    with pytest.raises(ValueError):
        _validate_email("user@examplecom")


def test_validate_email_rejects_empty():
    with pytest.raises(ValueError):
        _validate_email("")


def test_validate_email_rejects_non_string():
    with pytest.raises(TypeError):
        _validate_email(42)


# --- _validate_phone ---

def test_validate_phone_accepts_digits():
    assert _validate_phone("0041761234567") == "0041761234567"


def test_validate_phone_accepts_plus_prefix():
    assert _validate_phone("+41761234567") == "+41761234567"


def test_validate_phone_strips_whitespace():
    assert _validate_phone("  +41761234567  ") == "+41761234567"


def test_validate_phone_rejects_letters():
    with pytest.raises(ValueError):
        _validate_phone("abc123")


def test_validate_phone_rejects_empty():
    with pytest.raises(ValueError):
        _validate_phone("")


def test_validate_phone_rejects_non_string():
    with pytest.raises(TypeError):
        _validate_phone(41761234567)


# --- _validate_street ---

def test_validate_street_accepts_any_non_empty_string():
    assert _validate_street("Via Roma 1") == "Via Roma 1"


def test_validate_street_strips_whitespace():
    assert _validate_street("  Via Roma 1  ") == "Via Roma 1"


def test_validate_street_rejects_empty():
    with pytest.raises(ValueError):
        _validate_street("")


def test_validate_street_rejects_non_string():
    with pytest.raises(TypeError):
        _validate_street(123)


# --- _validate_city ---

def test_validate_city_accepts_valid():
    assert _validate_city("Milano") == "Milano"


def test_validate_city_rejects_empty():
    with pytest.raises(ValueError):
        _validate_city("")


def test_validate_city_rejects_digits():
    with pytest.raises(ValueError):
        _validate_city("Milan0")


# --- _validate_zip_code ---

def test_validate_zip_code_accepts_all_digits():
    assert _validate_zip_code("20100") == "20100"


def test_validate_zip_code_accepts_hyphenated():
    assert _validate_zip_code("10-100") == "10-100"


def test_validate_zip_code_rejects_starting_with_letter():
    with pytest.raises(ValueError):
        _validate_zip_code("AB123")


def test_validate_zip_code_rejects_empty():
    with pytest.raises(ValueError):
        _validate_zip_code("")


# --- _validate_country ---

def test_validate_country_accepts_valid():
    assert _validate_country("Italy") == "Italy"


def test_validate_country_rejects_empty():
    with pytest.raises(ValueError):
        _validate_country("")


# --- validate_text_field ---

def test_validate_text_field_accepts_valid():
    assert validate_text_field("Hello", "field", 10) == "Hello"


def test_validate_text_field_strips_whitespace():
    assert validate_text_field("  Hello  ", "field", 10) == "Hello"


def test_validate_text_field_rejects_empty():
    with pytest.raises(InvalidAttributeValueError):
        validate_text_field("", "field", 10)


def test_validate_text_field_rejects_whitespace_only():
    with pytest.raises(InvalidAttributeValueError):
        validate_text_field("   ", "field", 10)


def test_validate_text_field_rejects_over_max_length():
    with pytest.raises(InvalidAttributeValueError):
        validate_text_field("Hello", "field", 3)


def test_validate_text_field_accepts_exactly_max_length():
    result = validate_text_field("Hi!", "field", 3)
    assert result == "Hi!"


def test_validate_text_field_rejects_non_string():
    with pytest.raises(TypeError):
        validate_text_field(42, "field", 10)
