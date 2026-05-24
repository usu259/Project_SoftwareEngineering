import pytest
from datetime import date
from decimal import Decimal
from app.domain.work_report import WorkReport
from app.domain.position import PersonnelPosition, MaterialPosition
from app.domain.exceptions import DuplicatePositionError, PositionNotFoundError


@pytest.fixture
def report():
    return WorkReport(
        customer_id=1,
        employee_id=2,
        title="Garden maintenance",
        description="Mowed and trimmed",
        execution_date=date(2026, 5, 10),
    )


@pytest.fixture
def personnel():
    return PersonnelPosition(hours=Decimal("4"), hourly_rate=Decimal("25"), id=1)


@pytest.fixture
def material():
    return MaterialPosition(quantity=Decimal("3"), unit_price=Decimal("10"), id=2)


# --- Construction ---

def test_constructor_stores_fields(report):
    assert report.customer_id == 1
    assert report.employee_id == 2
    assert report.title == "Garden maintenance"
    assert report.execution_date == date(2026, 5, 10)


def test_constructor_rejects_non_int_customer_id():
    with pytest.raises(TypeError, match="customer_id"):
        WorkReport(customer_id="1", employee_id=2, title="T", description="D", execution_date=date.today())


def test_constructor_rejects_non_int_employee_id():
    with pytest.raises(TypeError, match="employee_id"):
        WorkReport(customer_id=1, employee_id=None, title="T", description="D", execution_date=date.today())


def test_constructor_rejects_non_date_execution_date():
    with pytest.raises(TypeError, match="execution_date"):
        WorkReport(customer_id=1, employee_id=2, title="T", description="D", execution_date="2026-01-01")


def test_constructor_rejects_empty_title():
    with pytest.raises(Exception):
        WorkReport(customer_id=1, employee_id=2, title="", description="D", execution_date=date.today())


def test_notes_defaults_to_none(report):
    assert report.notes is None


def test_invoice_id_defaults_to_none(report):
    assert report.invoice_id is None


# --- total_cost ---

def test_total_cost_is_zero_with_no_positions(report):
    assert report.total_cost == Decimal("0")


def test_total_cost_sums_all_positions(report, personnel, material):
    report.add_position(personnel)   # 4 * 25 = 100
    report.add_position(material)    # 3 * 10 = 30
    assert report.total_cost == Decimal("130")


# --- add_position ---

def test_add_position_appends(report, personnel):
    report.add_position(personnel)
    assert len(report.positions) == 1


def test_add_position_raises_on_duplicate_id(report, personnel):
    report.add_position(personnel)
    dup = PersonnelPosition(hours=Decimal("2"), hourly_rate=Decimal("10"), id=1)
    with pytest.raises(DuplicatePositionError):
        report.add_position(dup)


def test_add_position_allows_no_id_duplicates(report):
    p1 = PersonnelPosition(hours=Decimal("1"), hourly_rate=Decimal("10"))
    p2 = PersonnelPosition(hours=Decimal("2"), hourly_rate=Decimal("10"))
    report.add_position(p1)
    report.add_position(p2)
    assert len(report.positions) == 2


# --- remove_position ---

def test_remove_position_removes_by_id(report, personnel):
    report.add_position(personnel)
    report.remove_position(1)
    assert len(report.positions) == 0


def test_remove_position_raises_when_not_found(report):
    with pytest.raises(PositionNotFoundError):
        report.remove_position(999)


# --- positions returns a copy ---

def test_positions_returns_copy(report, personnel):
    report.add_position(personnel)
    snapshot = report.positions
    snapshot.clear()
    assert len(report.positions) == 1


# --- change methods ---

def test_change_title(report):
    report.change_title("New title")
    assert report.title == "New title"


def test_change_title_rejects_empty(report):
    with pytest.raises(Exception):
        report.change_title("")


def test_change_description(report):
    report.change_description("Updated description")
    assert report.description == "Updated description"


def test_change_notes(report):
    report.change_notes("Some note")
    assert report.notes == "Some note"


def test_change_notes_accepts_none(report):
    report.change_notes(None)
    assert report.notes is None


def test_change_execution_date(report):
    new_date = date(2026, 6, 1)
    report.change_execution_date(new_date)
    assert report.execution_date == new_date


def test_change_execution_date_rejects_string(report):
    with pytest.raises(TypeError):
        report.change_execution_date("2026-06-01")
