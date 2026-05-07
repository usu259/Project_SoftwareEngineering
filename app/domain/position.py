from abc import ABC, abstractmethod
from decimal import Decimal
from app.domain.exceptions import InvalidAttributeValueError


class Position(ABC):
    def __init__(
        self,
        id: int | None = None,
        description: str | None = None,
    ):
        self._id = id
        self._description = description

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def description(self) -> str | None:
        return self._description

    @property
    @abstractmethod
    def subtotal(self) -> Decimal:
        ...


class PersonnelPosition(Position):
    def __init__(
        self,
        hours: Decimal,
        hourly_rate: Decimal,
        id: int | None = None,
        description: str | None = None,
    ):
        super().__init__(id, description)
        if not isinstance(hours, Decimal) or hours <= 0:
            raise InvalidAttributeValueError("hours must be a positive Decimal")
        if not isinstance(hourly_rate, Decimal) or hourly_rate <= 0:
            raise InvalidAttributeValueError("hourly_rate must be a positive Decimal")
        self._hours = hours
        self._hourly_rate = hourly_rate

    @property
    def hours(self) -> Decimal:
        return self._hours

    @property
    def hourly_rate(self) -> Decimal:
        return self._hourly_rate

    @property
    def subtotal(self) -> Decimal:
        return self._hours * self._hourly_rate

    def __repr__(self) -> str:
        return f"PersonnelPosition(id={self._id!r}, hours={self._hours}, rate={self._hourly_rate})"


class MaterialPosition(Position):
    def __init__(
        self,
        quantity: Decimal,
        unit_price: Decimal,
        id: int | None = None,
        description: str | None = None,
    ):
        super().__init__(id, description)
        if not isinstance(quantity, Decimal) or quantity <= 0:
            raise InvalidAttributeValueError("quantity must be a positive Decimal")
        if not isinstance(unit_price, Decimal) or unit_price <= 0:
            raise InvalidAttributeValueError("unit_price must be a positive Decimal")
        self._quantity = quantity
        self._unit_price = unit_price

    @property
    def quantity(self) -> Decimal:
        return self._quantity

    @property
    def unit_price(self) -> Decimal:
        return self._unit_price

    @property
    def subtotal(self) -> Decimal:
        return self._quantity * self._unit_price

    def __repr__(self) -> str:
        return f"MaterialPosition(id={self._id!r}, quantity={self._quantity}, unit_price={self._unit_price})"
