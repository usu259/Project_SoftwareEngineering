import regex
from app.domain.exceptions import InvalidAttributeValueError

_NAME_REGEX = regex.compile(r"^[\p{L}\s'\-]+$")
_EMAIL_REGEX = regex.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_REGEX = regex.compile(r"^\+?\d+$")
_NAME_LIKE_REGEX = regex.compile(r"^[\p{L}\s'\-]+$")
_ZIP_CODE_REGEX = regex.compile(r"^[\d][\d\s\-]*$")


def _validate_name(value: str, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string, got {type(value).__name__}")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field} cannot be empty")
    if not _NAME_REGEX.match(normalized):
        raise ValueError(f"Invalid {field} format: {value!r}")
    return normalized


def _validate_email(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"email must be a string, got {type(value).__name__}")
    normalized = value.strip()
    if not normalized:
        raise ValueError("email cannot be empty")
    if not _EMAIL_REGEX.match(normalized):
        raise ValueError(f"Invalid email format: {value!r}")
    return normalized


def _validate_phone(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"phone must be a string, got {type(value).__name__}")
    normalized = value.strip()
    if not normalized:
        raise ValueError("phone cannot be empty")
    if not _PHONE_REGEX.match(normalized):
        raise ValueError(f"Invalid phone format: {value!r}")
    return normalized


def _validate_street(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"street must be a str, got {type(value).__name__}")
    normalized = value.strip()
    if not normalized:
        raise ValueError("street cannot be empty")
    return normalized


def _validate_city(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"city must be a str, got {type(value).__name__}")
    normalized = value.strip()
    if not normalized:
        raise ValueError("city cannot be empty")
    if not _NAME_LIKE_REGEX.match(normalized):
        raise ValueError(f"Invalid city format: {value!r}")
    return normalized


def _validate_zip_code(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"zip_code must be a str, got {type(value).__name__}")
    normalized = value.strip()
    if not normalized:
        raise ValueError("zip_code cannot be empty")
    if not _ZIP_CODE_REGEX.match(normalized):
        raise ValueError(f"Invalid zip_code format: {value!r}")
    return normalized


def _validate_country(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"country must be a str, got {type(value).__name__}")
    normalized = value.strip()
    if not normalized:
        raise ValueError("country cannot be empty")
    if not _NAME_LIKE_REGEX.match(normalized):
        raise ValueError(f"Invalid country format: {value!r}")
    return normalized


def validate_text_field(value: str, field: str, max_length: int) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string, got {type(value).__name__}")
    normalized = value.strip()
    if not normalized:
        raise InvalidAttributeValueError(f"{field} cannot be empty")
    if len(normalized) > max_length:
        raise InvalidAttributeValueError(
            f"{field} cannot exceed {max_length} characters, got {len(normalized)}"
        )
    return normalized
