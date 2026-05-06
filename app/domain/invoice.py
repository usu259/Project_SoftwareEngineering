from datetime import date
from decimal import Decimal
from enum import Enum, auto

from app.domain.work_report import WorkReport
from app.domain.exceptions import (
    InvalidAttributeValueError,
    CannotEditError,
    CannotDeleteError,
    InvalidStateChangeError,
    DuplicatePositionError,
    PositionNotFoundError,
)
from app.domain.validations import validate_text_field
from config import (
    MAX_INVOICE_TITLE_LENGTH,
    MAX_INVOICE_DESCRIPTION_LENGTH,
    MAX_INVOICE_NOTES_LENGTH,
)

_TAX_RATE = Decimal("1.081")


class InvoiceStatus(Enum):
    CREATED = auto()
    SENT = auto()
    PAID = auto()


class Invoice:

    def __init__(
        self,
        customer_id: int,
        title: str,
        description: str,
        notes: str | None = None,
        id: int | None = None,
        creation_date: date | None = None,
        status: InvoiceStatus | None = None,
        deleted: bool | None = None,
        work_reports: list[WorkReport] | None = None,
    ):
        self._id = id
        self._customer_id = customer_id
        self._title = validate_text_field(title, "title", MAX_INVOICE_TITLE_LENGTH)
        self._description = validate_text_field(description, "description", MAX_INVOICE_DESCRIPTION_LENGTH)
        self._notes = validate_text_field(notes, "notes", MAX_INVOICE_NOTES_LENGTH) if notes is not None else None
        self._creation_date = creation_date if creation_date is not None else date.today()
        self._status = status if status is not None else InvoiceStatus.CREATED
        self._deleted = deleted if deleted is not None else False
        self._work_reports: list[WorkReport] = work_reports if work_reports is not None else []

    # Properties
    @property
    def id(self) -> int | None:
        return self._id

    @property
    def customer_id(self) -> int:
        return self._customer_id

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
    def creation_date(self) -> date:
        return self._creation_date

    @property
    def status(self) -> InvoiceStatus:
        return self._status

    @property
    def deleted(self) -> bool:
        return self._deleted

    @property
    def work_reports(self) -> list[WorkReport]:
        return list(self._work_reports)

    # Derived properties
    @property
    def editable(self) -> bool:
        return not self._deleted and self._status is InvoiceStatus.CREATED

    @property
    def deletable(self) -> bool:
        return not self._deleted and self._status in (InvoiceStatus.CREATED, InvoiceStatus.PAID)

    @property
    def total_cost(self) -> Decimal:
        return sum((wr.total_cost for wr in self._work_reports), Decimal("0"))

    @property
    def total_cost_with_tax(self) -> Decimal:
        return self.total_cost * _TAX_RATE

    # Edit attributes
    def change_title(self, title: str) -> None:
        if not self.editable:
            raise CannotEditError("Invoice is not editable")
        self._title = validate_text_field(title, "title", MAX_INVOICE_TITLE_LENGTH)

    def change_description(self, description: str) -> None:
        if not self.editable:
            raise CannotEditError("Invoice is not editable")
        self._description = validate_text_field(description, "description", MAX_INVOICE_DESCRIPTION_LENGTH)

    def change_notes(self, notes: str) -> None:
        if not self.editable:
            raise CannotEditError("Invoice is not editable")
        self._notes = validate_text_field(notes, "notes", MAX_INVOICE_NOTES_LENGTH)

    # Work report management
    def add_work_report(self, work_report: WorkReport) -> None:
        if not self.editable:
            raise CannotEditError("Cannot add work reports to a non-editable invoice")
        if work_report.id is not None and any(wr.id == work_report.id for wr in self._work_reports):
            raise DuplicatePositionError(f"WorkReport {work_report.id} already exists in this invoice")
        self._work_reports.append(work_report)

    def remove_work_report(self, work_report_id: int) -> None:
        if not self.editable:
            raise CannotEditError("Cannot remove work reports from a non-editable invoice")
        match = next((wr for wr in self._work_reports if wr.id == work_report_id), None)
        if match is None:
            raise PositionNotFoundError(f"WorkReport {work_report_id} not found in this invoice")
        self._work_reports.remove(match)

    # Status management
    def change_status(self, status: InvoiceStatus) -> None:
        if self._deleted:
            raise CannotEditError("Cannot change status of a deleted invoice")
        if status is InvoiceStatus.CREATED:
            self._set_status_created()
        elif status is InvoiceStatus.SENT:
            self._set_status_sent()
        elif status is InvoiceStatus.PAID:
            self._set_status_paid()
        else:
            raise InvalidStateChangeError(f"Unknown status: {status!r}")

    def _set_status_created(self) -> None:
        raise InvalidStateChangeError("Cannot revert invoice to CREATED status")

    def _set_status_sent(self) -> None:
        if self._status is not InvoiceStatus.CREATED:
            raise InvalidStateChangeError("Invoice must be CREATED to be sent")
        if not self._work_reports:
            raise InvalidStateChangeError("Cannot send an invoice with no work reports")
        self._status = InvoiceStatus.SENT

    def _set_status_paid(self) -> None:
        if self._status is not InvoiceStatus.SENT:
            raise InvalidStateChangeError("Invoice must be SENT before it can be marked as paid")
        self._status = InvoiceStatus.PAID

    # Deletion
    def mark_deleted(self) -> None:
        if not self.deletable:
            raise CannotDeleteError("Invoice cannot be deleted in its current state")
        self._deleted = True

    # Representation
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Invoice):
            return NotImplemented
        if self._id is None or other._id is None:
            return self is other
        return self._id == other._id

    __hash__ = None

    def __repr__(self) -> str:
        return f"<Invoice #{self._id} | {self._status.name} | total: {self.total_cost}>"
