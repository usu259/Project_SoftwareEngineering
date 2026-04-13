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
        role: EmployeeRole,
        id: int | None = None,
    ):
        super().__init__(first_name, last_name, email)
        self._role = self._validate_role(role)
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

    @staticmethod
    def _validate_role(value: EmployeeRole) -> EmployeeRole:
        if not isinstance(value, EmployeeRole):
            raise TypeError(
                f"role must be an EmployeeRole, got {type(value).__name__}"
            )
        return value