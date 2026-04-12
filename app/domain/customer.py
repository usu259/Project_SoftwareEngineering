import regex
from app.domain.person import Person
from app.domain.value_objects import Address


class Customer(Person):
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
        super().__init__(first_name, last_name, email)
        self._phone = self._validate_phone(phone)
        self._address = self._validate_address(address)
        self._id = id

    @property
    def phone(self) -> str:
        return self._phone

    @property
    def address(self) -> Address:
        return self._address

    @property
    def id(self) -> int | None:
        return self._id

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

    def update_address(self, address: Address) -> None:
        """Replace the address with a new one."""
        self._address = self._validate_address(address)

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