import pytest
from app.domain.employee import Employee, EmployeeRole


@pytest.fixture
def employee():
    return Employee("Mario", "Rossi", "mario@example.com", "+41765742923", EmployeeRole.GARDENER)


def test_constructor_sets_role(employee):
    assert employee.role is EmployeeRole.GARDENER


def test_constructor_strips_whitespace_from_first_name():
    e = Employee("  Anna  ", "Bianchi", "a@b.com", "+41700000001", EmployeeRole.BRICKLAYER)
    assert e.first_name == "Anna"


def test_constructor_rejects_empty_last_name():
    with pytest.raises(ValueError, match="last_name"):
        Employee("Mario", "", "m@r.com", "+41700000001", EmployeeRole.GARDENER)


def test_constructor_rejects_invalid_role():
    with pytest.raises(TypeError, match="role"):
        Employee("Mario", "Rossi", "m@r.com", "+41700000001", "gardener")


def test_constructor_rejects_non_int_id():
    with pytest.raises(TypeError, match="id"):
        Employee("Mario", "Rossi", "m@r.com", "+41700000001", EmployeeRole.GARDENER, id="1")


def test_constructor_accepts_none_id(employee):
    assert employee.id is None


def test_constructor_accepts_int_id():
    e = Employee("Mario", "Rossi", "m@r.com", "+41700000001", EmployeeRole.GARDENER, id=42)
    assert e.id == 42


def test_update_role_changes_role(employee):
    employee.update_role(EmployeeRole.OWNER)
    assert employee.role is EmployeeRole.OWNER


def test_update_role_rejects_string():
    e = Employee("Mario", "Rossi", "m@r.com", "+41700000001", EmployeeRole.GARDENER)
    with pytest.raises(TypeError, match="role"):
        e.update_role("owner")


def test_full_name_returns_first_and_last(employee):
    assert employee.full_name == "Mario Rossi"


def test_equality_by_id():
    e1 = Employee("Mario", "Rossi", "a@b.com", "+41700000001", EmployeeRole.GARDENER, id=1)
    e2 = Employee("Mario", "Rossi", "a@b.com", "+41700000001", EmployeeRole.GARDENER, id=1)
    assert e1 == e2


def test_inequality_different_ids():
    e1 = Employee("Mario", "Rossi", "a@b.com", "+41700000001", EmployeeRole.GARDENER, id=1)
    e2 = Employee("Mario", "Rossi", "a@b.com", "+41700000001", EmployeeRole.GARDENER, id=2)
    assert e1 != e2


def test_equality_without_id_uses_identity():
    e1 = Employee("Mario", "Rossi", "a@b.com", "+41700000001", EmployeeRole.GARDENER)
    e2 = Employee("Mario", "Rossi", "a@b.com", "+41700000001", EmployeeRole.GARDENER)
    assert e1 != e2
    assert e1 == e1


def test_update_name_changes_first_and_last(employee):
    employee.update_name(first_name="Luigi", last_name="Verdi")
    assert employee.first_name == "Luigi"
    assert employee.last_name == "Verdi"


def test_all_roles_are_valid():
    for role in EmployeeRole:
        e = Employee("Mario", "Rossi", "m@r.com", "+41700000001", role)
        assert e.role is role
