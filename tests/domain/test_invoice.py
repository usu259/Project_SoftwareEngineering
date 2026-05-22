import pytest
from datetime import date
from decimal import Decimal
from app.domain.invoice import Invoice, InvoiceStatus
from app.domain.work_report import WorkReport
from app.domain.position import PersonnelPosition
from app.domain.exceptions import (
    CannotEditError,
    CannotDeleteError,
    InvalidStateChangeError,
    DuplicatePositionError,
    PositionNotFoundError,
)
from config import TAX_RATE


def make_work_report(wr_id=1, total=Decimal("100")):
    """Helper: a WorkReport with one personnel position giving the requested total."""
    wr = WorkReport(
        customer_id=1,
        employee_id=1,
        title="Work",
        description="Desc",
        execution_date=date(2026, 5, 1),
        id=wr_id,
    )
    pos = PersonnelPosition(hours=total, hourly_rate=Decimal("1"), id=wr_id * 10)
    wr.add_position(pos)
    return wr


@pytest.fixture
def invoice():
    return Invoice(customer_id=1, title="May Invoice", description="May work")


@pytest.fixture
def invoice_with_report(invoice):
    invoice.add_work_report(make_work_report(wr_id=1, total=Decimal("200")))
    return invoice


# --- Construction ---

def test_constructor_defaults_status_to_created(invoice):
    assert invoice.status is InvoiceStatus.CREATED


def test_constructor_defaults_deleted_to_false(invoice):
    assert invoice.deleted is False


def test_constructor_defaults_creation_date_to_today(invoice):
    assert invoice.creation_date == date.today()


def test_constructor_stores_customer_id(invoice):
    assert invoice.customer_id == 1


def test_constructor_stores_title(invoice):
    assert invoice.title == "May Invoice"


def test_constructor_notes_defaults_to_none(invoice):
    assert invoice.notes is None


# --- editable / deletable ---

def test_editable_when_created_and_not_deleted(invoice):
    assert invoice.editable is True


def test_not_editable_when_sent(invoice_with_report):
    invoice_with_report.change_status(InvoiceStatus.SENT)
    assert invoice_with_report.editable is False


def test_not_editable_when_deleted(invoice):
    invoice.mark_deleted()
    assert invoice.editable is False


def test_deletable_when_created(invoice):
    assert invoice.deletable is True


def test_deletable_when_paid(invoice_with_report):
    invoice_with_report.change_status(InvoiceStatus.SENT)
    invoice_with_report.change_status(InvoiceStatus.PAID)
    assert invoice_with_report.deletable is True


def test_not_deletable_when_sent(invoice_with_report):
    invoice_with_report.change_status(InvoiceStatus.SENT)
    assert invoice_with_report.deletable is False


def test_not_deletable_when_already_deleted(invoice):
    invoice.mark_deleted()
    assert invoice.deletable is False


# --- total_cost and tax ---

def test_total_cost_zero_with_no_reports(invoice):
    assert invoice.total_cost == Decimal("0")


def test_total_cost_sums_work_reports(invoice):
    invoice.add_work_report(make_work_report(wr_id=1, total=Decimal("100")))
    invoice.add_work_report(make_work_report(wr_id=2, total=Decimal("50")))
    assert invoice.total_cost == Decimal("150")


def test_total_cost_with_tax(invoice):
    invoice.add_work_report(make_work_report(wr_id=1, total=Decimal("100")))
    assert invoice.total_cost_with_tax == Decimal("100") * TAX_RATE


# --- change_title / change_description / change_notes ---

def test_change_title_updates_title(invoice):
    invoice.change_title("June Invoice")
    assert invoice.title == "June Invoice"


def test_change_title_raises_when_not_editable(invoice_with_report):
    invoice_with_report.change_status(InvoiceStatus.SENT)
    with pytest.raises(CannotEditError):
        invoice_with_report.change_title("New")


def test_change_description_updates(invoice):
    invoice.change_description("New description")
    assert invoice.description == "New description"


def test_change_notes_updates(invoice):
    invoice.change_notes("A note")
    assert invoice.notes == "A note"


def test_change_notes_raises_when_not_editable(invoice_with_report):
    invoice_with_report.change_status(InvoiceStatus.SENT)
    with pytest.raises(CannotEditError):
        invoice_with_report.change_notes("note")


# --- add_work_report / remove_work_report ---

def test_add_work_report_appends(invoice):
    wr = make_work_report(wr_id=1)
    invoice.add_work_report(wr)
    assert len(invoice.work_reports) == 1


def test_add_work_report_raises_on_duplicate(invoice):
    wr = make_work_report(wr_id=1)
    invoice.add_work_report(wr)
    with pytest.raises(DuplicatePositionError):
        invoice.add_work_report(wr)


def test_add_work_report_raises_when_not_editable(invoice_with_report):
    invoice_with_report.change_status(InvoiceStatus.SENT)
    with pytest.raises(CannotEditError):
        invoice_with_report.add_work_report(make_work_report(wr_id=99))


def test_remove_work_report_removes(invoice_with_report):
    invoice_with_report.remove_work_report(1)
    assert len(invoice_with_report.work_reports) == 0


def test_remove_work_report_raises_when_not_found(invoice):
    with pytest.raises(PositionNotFoundError):
        invoice.remove_work_report(999)


def test_remove_work_report_raises_when_not_editable(invoice_with_report):
    invoice_with_report.change_status(InvoiceStatus.SENT)
    with pytest.raises(CannotEditError):
        invoice_with_report.remove_work_report(1)


def test_work_reports_returns_copy(invoice_with_report):
    snapshot = invoice_with_report.work_reports
    snapshot.clear()
    assert len(invoice_with_report.work_reports) == 1


# --- state machine ---

def test_send_transitions_to_sent(invoice_with_report):
    invoice_with_report.change_status(InvoiceStatus.SENT)
    assert invoice_with_report.status is InvoiceStatus.SENT


def test_send_raises_without_work_reports(invoice):
    with pytest.raises(InvalidStateChangeError):
        invoice.change_status(InvoiceStatus.SENT)


def test_send_raises_when_already_sent(invoice_with_report):
    invoice_with_report.change_status(InvoiceStatus.SENT)
    with pytest.raises(InvalidStateChangeError):
        invoice_with_report.change_status(InvoiceStatus.SENT)


def test_pay_transitions_to_paid(invoice_with_report):
    invoice_with_report.change_status(InvoiceStatus.SENT)
    invoice_with_report.change_status(InvoiceStatus.PAID)
    assert invoice_with_report.status is InvoiceStatus.PAID


def test_pay_raises_if_not_sent(invoice_with_report):
    with pytest.raises(InvalidStateChangeError):
        invoice_with_report.change_status(InvoiceStatus.PAID)


def test_cannot_revert_to_created(invoice_with_report):
    invoice_with_report.change_status(InvoiceStatus.SENT)
    with pytest.raises(InvalidStateChangeError):
        invoice_with_report.change_status(InvoiceStatus.CREATED)


def test_change_status_raises_on_deleted_invoice(invoice):
    invoice.mark_deleted()
    with pytest.raises(CannotEditError):
        invoice.change_status(InvoiceStatus.SENT)


# --- mark_deleted ---

def test_mark_deleted_sets_deleted_true(invoice):
    invoice.mark_deleted()
    assert invoice.deleted is True


def test_mark_deleted_raises_when_sent(invoice_with_report):
    invoice_with_report.change_status(InvoiceStatus.SENT)
    with pytest.raises(CannotDeleteError):
        invoice_with_report.mark_deleted()


def test_mark_deleted_raises_when_already_deleted(invoice):
    invoice.mark_deleted()
    with pytest.raises(CannotDeleteError):
        invoice.mark_deleted()
