from datetime import date
from decimal import Decimal
from domain.position import Position


class WorkReport:
    def __init__(
        self,
        customer_id: int,
        employee_id: int,
        title: str,
        description: str,
        execution_date: date,
        notes: str | None = None,
        invoice_id: int | None = None,
        id: int | None = None,
        positions: list[Position] | None = None,
    ):
        self._id = id
        self._customer_id = customer_id
        self._employee_id = employee_id
        self._invoice_id = invoice_id
        self._title = title
        self._description = description
        self._notes = notes
        self._execution_date = execution_date
        self._positions: list[Position] = positions if positions is not None else []

    # --- Properties ---
    @property
    def id(self) -> int | None:
        return self._id

    @property
    def customer_id(self) -> int:
        return self._customer_id

    @property
    def employee_id(self) -> int:
        return self._employee_id

    @property
    def invoice_id(self) -> int | None:
        return self._invoice_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def notes(self) -> str | None:
        return self._notes

    @property
    def execution_date(self) -> date:
        return self._execution_date

    @property
    def positions(self) -> list[Position]:
        return list(self._positions)

    # --- Domain logic ---
    @property
    def total_cost(self) -> Decimal:
        return sum((p.subtotal for p in self._positions), Decimal("0"))

    def add_position(self, position: Position) -> None:
        if any(p.id == position.id for p in self._positions):
            raise ValueError(f"Position {position.id} already exists in this WorkReport")
        self._positions.append(position)

    def remove_position(self, position_id: int) -> None:
        match = next((p for p in self._positions if p.id == position_id), None)
        if match is None:
            raise ValueError(f"Position {position_id} not found in this WorkReport")
        self._positions.remove(match)

    def __repr__(self) -> str:
        return f"<WorkReport '{self._title}' | {self._execution_date} | total: {self.total_cost}>"