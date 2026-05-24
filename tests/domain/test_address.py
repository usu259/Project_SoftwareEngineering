import pytest
from app.domain.value_objects import Address


@pytest.fixture
def address():
    return Address(street="main street", city="zurich", zip_code="8050", country="switzerland")


def test_constructor_stores_fields(address):
    assert address.street == "main street"
    assert address.city == "zurich"
    assert address.zip_code == "8050"
    assert address.country == "switzerland"


def test_address_is_immutable(address):
    with pytest.raises((AttributeError, TypeError)):
        address.street = "Via Nuova 2"


def test_equality_by_value():
    a1 = Address(street="main street", city="zurich", zip_code="8050", country="switzerland")
    a2 = Address(street="main street", city="zurich", zip_code="8050", country="switzerland")
    assert a1 == a2


def test_inequality_when_fields_differ():
    a1 = Address(street="main street", city="zurich", zip_code="8050", country="switzerland")
    a2 = Address(street="Via Verdi 2", city="zurich", zip_code="8050", country="switzerland")
    assert a1 != a2


def test_strips_whitespace_from_street():
    a = Address(street="  main street  ", city="zurich", zip_code="8050", country="switzerland")
    assert a.street == "main street"


def test_rejects_empty_street():
    with pytest.raises(ValueError):
        Address(street="", city="zurich", zip_code="8050", country="switzerland")


def test_rejects_empty_city():
    with pytest.raises(ValueError):
        Address(street="main street", city="", zip_code="8050", country="switzerland")


def test_rejects_empty_zip_code():
    with pytest.raises(ValueError):
        Address(street="main street", city="zurich", zip_code="", country="switzerland")


def test_rejects_zip_code_not_starting_with_digit():
    with pytest.raises(ValueError):
        Address(street="main street", city="zurich", zip_code="AB123", country="switzerland")


def test_rejects_empty_country():
    with pytest.raises(ValueError):
        Address(street="main street", city="zurich", zip_code="8050", country="")


def test_accepts_hyphenated_zip_code():
    a = Address(street="main street", city="zurich", zip_code="10-100", country="switzerland")
    assert a.zip_code == "10-100"


def test_accepts_unicode_city():
    a = Address(street="main street", city="Zürich", zip_code="8001", country="Switzerland")
    assert a.city == "Zürich"