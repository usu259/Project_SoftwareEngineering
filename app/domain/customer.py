import regex
from app.domain.value_objects import Address


class Customer:
    EMAIL_REGEX = regex.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    NAME_REGEX = regex.compile(r"^[\p{L}\s'\-]+$")
    PHONE_REGEX = regex.compile(r"^\+?\d+$")

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: Address,
        id: int | None = None,
    ):
        self._first_name = self._validate_name(first_name, field="first_name")
        self._last_name = self._validate_name(last_name, field="last_name")
        self._email = self._validate_email(email)
        self._phone = self._validate_phone(phone)
        self._address = self._validate_address(address)
        self._id = id

    # Properties: Read-only access. Make sure that param cannot be changed without validation

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
    def address(self) -> Address:
        return self._address

    @property
    def id(self) -> int | None:
        return self._id

    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"

    # Methods

    def update_contact(
        self, email: str | None = None, phone: str | None = None
    ) -> None:
        """Update email, phone, or both. Atomic: either all succeed or none."""
        if email is None and phone is None:
            raise ValueError("At least one field (email or phone) must be provided")

        new_email = self._validate_email(email) if email is not None else None
        new_phone = self._validate_phone(phone) if phone is not None else None

        if email is not None:
            self._email = new_email
        if phone is not None:
            self._phone = new_phone

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

    def update_address(self, address: Address) -> None:
        """Replace the address with a new one."""
        self._address = self._validate_address(address)

    # Private validators

    @staticmethod
    def _validate_name(value: str, field: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{field} must be a string, got {type(value).__name__}")
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{field} cannot be empty")
        if not Customer.NAME_REGEX.match(normalized):
            raise ValueError(f"Invalid {field} format: {value!r}")
        return normalized

    @staticmethod
    def _validate_email(value: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"email must be a string, got {type(value).__name__}")
        normalized = value.strip()
        if not normalized:
            raise ValueError("email cannot be empty")
        if not Customer.EMAIL_REGEX.match(normalized):
            raise ValueError(f"Invalid email format: {value!r}")
        return normalized

    @staticmethod
    def _validate_phone(value: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"phone must be a string, got {type(value).__name__}")
        normalized = value.strip()
        if not normalized:
            raise ValueError("phone cannot be empty")
        if not Customer.PHONE_REGEX.match(normalized):
            raise ValueError(f"Invalid phone format: {value!r}")
        return normalized

    @staticmethod
    def _validate_address(value: Address) -> Address:
        if not isinstance(value, Address):
            raise TypeError(f"address must be an Address, got {type(value).__name__}")
        return value





