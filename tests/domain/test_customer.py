import pytest
from app.domain.customer import Customer
from app.domain.value_objects import Address


@pytest.fixture
def address():
    return Address(street="via capuana", city="rho", zip_code="20017", country="italy")


@pytest.fixture
def customer(address):
    return Customer("Mario", "Rossi", "m@r.com", "+41765742923", address)


def test_constructor_strips_whitespace_from_first_name(address):
    customer = Customer("  Mario  ", "Rossi", "m@r.com", "+41765742923", address)
    assert customer.first_name == "Mario"

def test_constructor_rejects_empty_first_name(address):
    with pytest.raises(ValueError, match="first_name"):
        Customer("", "Rossi", "m@r.com", "+41765742923", address)

def test_constructor_accepts_unicode_names(address):
    customer = Customer("Müller", "O'Brien", "m@r.com", "+41765742923", address)
    assert customer.first_name == "Müller"
    assert customer.last_name == "O'Brien"

def test_constructor_rejects_non_address_for_address_field():
    with pytest.raises(TypeError, match="address"):
        Customer("Mario", "Rossi", "m@r.com", "+41765742923", "not an address")

def test_update_contact_is_atomic_on_partial_failure(customer):
    # email valida ma phone invalido → deve fallire SENZA toccare l'email
    with pytest.raises(ValueError):
        customer.update_contact(email="valid@example.com", phone="NOT_VALID")
    assert customer.email == "m@r.com"


def test_update_contact_updates_both_fields(customer):
    customer.update_contact(email="new@example.com", phone="+41799999999")
    assert customer.email == "new@example.com"
    assert customer.phone == "+41799999999"

def test_update_contact_strips_whitespace_from_email(customer):
    customer.update_contact(email="  spaced@example.com  ")
    assert customer.email == "spaced@example.com"


def test_full_name_returns_first_and_last_name_with_space(customer):
    assert customer.full_name() == "Mario Rossi"

