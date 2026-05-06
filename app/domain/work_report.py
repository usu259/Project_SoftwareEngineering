from datetime import date
from decimal import Decimal
from app.domain.position import Position
from app.domain.exceptions import DuplicatePositionError, PositionNotFoundError
from app.domain.validations import validate_text_field
from config import MAX_WORK_REPORT_TITLE_LENGTH, MAX_WORK_REPORT_DESCRIPTION_LENGTH, MAX_WORK_REPORT_NOTES_LENGTH


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
        if not isinstance(customer_id, int):
            raise TypeError(f"customer_id must be an int, got {type(customer_id).__name__}")
        if not isinstance(employee_id, int):
            raise TypeError(f"employee_id must be an int, got {type(employee_id).__name__}")
        if not isinstance(execution_date, date):
            raise TypeError(f"execution_date must be a date, got {type(execution_date).__name__}")
        self._id = id
        self._customer_id = customer_id
        self._employee_id = employee_id
        self._invoice_id = invoice_id
        self._title = validate_text_field(title, "title", MAX_WORK_REPORT_TITLE_LENGTH)
        self._description = validate_text_field(description, "description", MAX_WORK_REPORT_DESCRIPTION_LENGTH)
        self._notes = validate_text_field(notes, "notes", MAX_WORK_REPORT_NOTES_LENGTH) if notes is not None else None
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
        if position.id is not None and any(p.id == position.id for p in self._positions):
            raise DuplicatePositionError(f"Position {position.id} already exists in this WorkReport")
        self._positions.append(position)

    def remove_position(self, position_id: int) -> None:
        match = next((p for p in self._positions if p.id == position_id), None)
        if match is None:
            raise PositionNotFoundError(f"Position {position_id} not found in this WorkReport")
        self._positions.remove(match)

    def __repr__(self) -> str:
        return f"<WorkReport '{self._title}' | {self._execution_date} | total: {self.total_cost}>"
