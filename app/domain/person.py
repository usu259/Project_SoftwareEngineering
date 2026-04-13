import regex
from abc import ABC, abstractmethod


class Person(ABC):
    NAME_REGEX = regex.compile(r"^[\p{L}\s'\-]+$")
    EMAIL_REGEX = regex.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    PHONE_REGEX = regex.compile(r"^\+?\d+$")

    def __init__(self, first_name: str, last_name: str, email: str, phone: str):
        self._first_name = self._validate_name(first_name, field="first_name")
        self._last_name = self._validate_name(last_name, field="last_name")
        self._email = self._validate_email(email)
        self._phone = self._validate_phone(phone)

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def email(self) -> str:
        return self._email

    @property
    def phone(self) -> str:
        return self._phone

    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"

    @abstractmethod
    def __repr__(self) -> str: ...

    def update_name(
        self, first_name: str | None = None, last_name: str | None = None
    ) -> None:
        """Update first name, last name, or both. Atomic."""
        if first_name is None and last_name is None:
            raise ValueError("At least one field (first_name or last_name) must be provided")

        new_first = self._validate_name(first_name, field="first_name") if first_name is not None else None
        new_last = self._validate_name(last_name, field="last_name") if last_name is not None else None

        if first_name is not None:
            self._first_name = new_first
        if last_name is not None:
            self._last_name = new_last

    def update_email(self, email: str) -> None:
        """Replace the email."""
        self._email = self._validate_email(email)

    def update_phone(self, phone: str) -> None:
        """Replace the phone."""
        self._phone = self._validate_phone(phone)

    @staticmethod
    def _validate_name(value: str, field: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{field} must be a string, got {type(value).__name__}")
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{field} cannot be empty")
        if not Person.NAME_REGEX.match(normalized):
            raise ValueError(f"Invalid {field} format: {value!r}")
        return normalized

    @staticmethod
    def _validate_email(value: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"email must be a string, got {type(value).__name__}")
        normalized = value.strip()
        if not normalized:
            raise ValueError("email cannot be empty")
        if not Person.EMAIL_REGEX.match(normalized):
            raise ValueError(f"Invalid email format: {value!r}")
        return normalized

    @staticmethod
    def _validate_phone(value: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"phone must be a string, got {type(value).__name__}")
        normalized = value.strip()
        if not normalized:
            raise ValueError("phone cannot be empty")
        if not Person.PHONE_REGEX.match(normalized):
            raise ValueError(f"Invalid phone format: {value!r}")
        return normalized
