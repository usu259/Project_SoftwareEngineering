from sqlalchemy.orm import Session

from app.domain.employee import Employee, EmployeeRole
from app.repositories.employee_repository import EmployeeRepository


class EmployeeService:
    def __init__(self, session: Session):
        self._session = session
        self._repo = EmployeeRepository(session)

    def create_employee(
        self,
        first_name: str,
        last_name: str,
        email: str,
        role: EmployeeRole,
    ) -> Employee:
        if self._repo.get_by_email(email) is not None:
            raise ValueError(f"Email {email!r} is already in use")

        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
        )
        self._repo.save(employee)
        self._session.flush()
        return employee

    def get_employee(self, employee_id: int) -> Employee:
        employee = self._repo.get_by_id(employee_id)
        if employee is None:
            raise ValueError(f"Employee with id {employee_id!r} not found")
        return employee

    def get_all_employees(self) -> list[Employee]:
        return self._repo.get_all()

    def get_employees_by_role(self, role: EmployeeRole) -> list[Employee]:
        return self._repo.get_by_role(role)

    def update_employee_name(
        self,
        employee_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> Employee:
        employee = self.get_employee(employee_id)
        employee.update_name(first_name=first_name, last_name=last_name)
        return employee

    def update_employee_email(self, employee_id: int, email: str) -> Employee:
        employee = self.get_employee(employee_id)

        if email != employee.email:
            if self._repo.get_by_email(email) is not None:
                raise ValueError(f"Email {email!r} is already in use")

        employee.update_email(email)
        return employee

    def update_employee_role(
        self, employee_id: int, role: EmployeeRole
    ) -> Employee:
        employee = self.get_employee(employee_id)
        employee.update_role(role)
        return employee

    def delete_employee(self, employee_id: int) -> None:
        employee = self.get_employee(employee_id)
        self._repo.delete(employee)