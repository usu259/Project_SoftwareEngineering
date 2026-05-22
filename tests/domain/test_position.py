import pytest
from decimal import Decimal
from app.domain.position import PersonnelPosition, MaterialPosition
from app.domain.exceptions import InvalidAttributeValueError


# --- PersonnelPosition ---

def test_personnel_subtotal():
    p = PersonnelPosition(hours=Decimal("8"), hourly_rate=Decimal("50"))
    assert p.subtotal == Decimal("400")


def test_personnel_stores_hours_and_rate():
    p = PersonnelPosition(hours=Decimal("3.5"), hourly_rate=Decimal("20"))
    assert p.hours == Decimal("3.5")
    assert p.hourly_rate == Decimal("20")


def test_personnel_rejects_zero_hours():
    with pytest.raises(InvalidAttributeValueError):
        PersonnelPosition(hours=Decimal("0"), hourly_rate=Decimal("50"))


def test_personnel_rejects_negative_hours():
    with pytest.raises(InvalidAttributeValueError):
        PersonnelPosition(hours=Decimal("-1"), hourly_rate=Decimal("50"))


def test_personnel_rejects_zero_rate():
    with pytest.raises(InvalidAttributeValueError):
        PersonnelPosition(hours=Decimal("8"), hourly_rate=Decimal("0"))


def test_personnel_rejects_negative_rate():
    with pytest.raises(InvalidAttributeValueError):
        PersonnelPosition(hours=Decimal("8"), hourly_rate=Decimal("-10"))


def test_personnel_rejects_float_hours():
    with pytest.raises(InvalidAttributeValueError):
        PersonnelPosition(hours=8.0, hourly_rate=Decimal("50"))


def test_personnel_rejects_float_rate():
    with pytest.raises(InvalidAttributeValueError):
        PersonnelPosition(hours=Decimal("8"), hourly_rate=50.0)


def test_personnel_stores_optional_description():
    p = PersonnelPosition(hours=Decimal("4"), hourly_rate=Decimal("30"), description="Mowing")
    assert p.description == "Mowing"


def test_personnel_stores_optional_id():
    p = PersonnelPosition(hours=Decimal("4"), hourly_rate=Decimal("30"), id=7)
    assert p.id == 7


def test_personnel_description_defaults_to_none():
    p = PersonnelPosition(hours=Decimal("4"), hourly_rate=Decimal("30"))
    assert p.description is None


# --- MaterialPosition ---

def test_material_subtotal():
    m = MaterialPosition(quantity=Decimal("10"), unit_price=Decimal("3.50"))
    assert m.subtotal == Decimal("35.00")


def test_material_stores_quantity_and_price():
    m = MaterialPosition(quantity=Decimal("5"), unit_price=Decimal("12"))
    assert m.quantity == Decimal("5")
    assert m.unit_price == Decimal("12")


def test_material_rejects_zero_quantity():
    with pytest.raises(InvalidAttributeValueError):
        MaterialPosition(quantity=Decimal("0"), unit_price=Decimal("10"))


def test_material_rejects_negative_unit_price():
    with pytest.raises(InvalidAttributeValueError):
        MaterialPosition(quantity=Decimal("5"), unit_price=Decimal("-1"))


def test_material_rejects_float_quantity():
    with pytest.raises(InvalidAttributeValueError):
        MaterialPosition(quantity=5.0, unit_price=Decimal("10"))


def test_material_stores_optional_description():
    m = MaterialPosition(quantity=Decimal("2"), unit_price=Decimal("15"), description="Cement bag")
    assert m.description == "Cement bag"


def test_material_stores_optional_id():
    m = MaterialPosition(quantity=Decimal("2"), unit_price=Decimal("15"), id=99)
    assert m.id == 99
