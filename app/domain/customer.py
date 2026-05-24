from app.domain.person import Person
from app.domain.value_objects import Address
from app.domain.validations import _validate_email, _validate_phone


class Customer(Person):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: Address,
        id: int | None = None,
    ):
        super().__init__(first_name, last_name, email, phone)
        self._address = self._validate_address(address)
        if id is not None and not isinstance(id, int):
            raise TypeError(f"id must be an int, got {type(id).__name__}")
        self._id = id

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

        new_email = _validate_email(email) if email is not None else None
        new_phone = _validate_phone(phone) if phone is not None else None

        if email is not None:
            self._email = new_email
        if phone is not None:
            self._phone = new_phone

    def update_address(self, address: Address) -> None:
        self._address = self._validate_address(address)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Customer):
            return NotImplemented
        if self._id is None or other._id is None:
            return self is other
        return self._id == other._id

    __hash__ = None

    def __repr__(self) -> str:
        return f"Customer(id={self._id!r}, email={self._email!r})"

    def __str__(self) -> str:
        return f"{self.full_name} ({self._email})"

    @staticmethod
    def _validate_address(value: Address) -> Address:
        if not isinstance(value, Address):
            raise TypeError(f"address must be an Address, got {type(value).__name__}")
        return value
