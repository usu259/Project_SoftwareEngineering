from enum import Enum
from app.domain.person import Person


class EmployeeRole(Enum):
    GARDENER = "gardener"
    BRICKLAYER = "bricklayer"
    OWNER = "owner"


class Employee(Person):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        role: EmployeeRole,
        id: int | None = None,
    ):
        super().__init__(first_name, last_name, email, phone)
        self._role = self._validate_role(role)
        if id is not None and not isinstance(id, int):
            raise TypeError(f"id must be an int, got {type(id).__name__}")
        self._id = id

    @property
    def role(self) -> EmployeeRole:
        return self._role

    @property
    def id(self) -> int | None:
        return self._id

    def update_role(self, role: EmployeeRole) -> None:
        """Replace the role."""
        self._role = self._validate_role(role)


    __hash__ = None

    def __eq__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented
        if self._id is None or other._id is None:
            return self is other
        return self._id == other._id

    def __repr__(self):
        return f"Employee(id={self._id!r}, email={self._email!r}, role={self._role!r})"

    def __str__(self):
        return f"{self._first_name} {self._last_name} ({self._role.value})"

    
    @staticmethod
    def _validate_role(value: EmployeeRole) -> EmployeeRole:
        if not isinstance(value, EmployeeRole):
            raise TypeError(
                f"role must be an EmployeeRole, got {type(value).__name__}"
            )
        return value