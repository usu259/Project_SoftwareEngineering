from decimal import Decimal
from app.domain.employee import EmployeeRole
from app.domain.exceptions import InvalidAttributeValueError


class EmployeeRate:
    def __init__(
        self,
        name: str,
        unit_price: Decimal,
        role: EmployeeRole,
        id: int | None = None,
    ):
        if not isinstance(name, str) or not name.strip():
            raise InvalidAttributeValueError("name must be a non-empty string")
        if not isinstance(unit_price, Decimal) or unit_price <= 0:
            raise InvalidAttributeValueError("unit_price must be a positive Decimal")
        if id is not None and not isinstance(id, int):
            raise TypeError(f"id must be an int, got {type(id).__name__}")
        self._id = id
        self._name = name.strip()
        self._unit_price = unit_price
        self._role = self._validate_role(role)

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def unit_price(self) -> Decimal:
        return self._unit_price

    @property
    def role(self) -> EmployeeRole:
        return self._role

    def update_role(self, role: EmployeeRole) -> None:
        self._role = self._validate_role(role)

    def __repr__(self) -> str:
        return f"EmployeeRate(id={self._id!r}, name={self._name!r}, role={self._role!r})"

    @staticmethod
    def _validate_role(value: EmployeeRole) -> EmployeeRole:
        if not isinstance(value, EmployeeRole):
            raise TypeError(f"role must be an EmployeeRole, got {type(value).__name__}")
        return value
