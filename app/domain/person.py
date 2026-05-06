from abc import ABC, abstractmethod
from app.domain.validations import _validate_name, _validate_email, _validate_phone


class Person(ABC):
    def __init__(self, first_name: str, last_name: str, email: str, phone: str):
        self._first_name = _validate_name(first_name, field="first_name")
        self._last_name = _validate_name(last_name, field="last_name")
        self._email = _validate_email(email)
        self._phone = _validate_phone(phone)

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

        new_first = _validate_name(first_name, field="first_name") if first_name is not None else None
        new_last = _validate_name(last_name, field="last_name") if last_name is not None else None

        if first_name is not None:
            self._first_name = new_first
        if last_name is not None:
            self._last_name = new_last

    def update_email(self, email: str) -> None:
        self._email = _validate_email(email)

    def update_phone(self, phone: str) -> None:
        self._phone = _validate_phone(phone)
