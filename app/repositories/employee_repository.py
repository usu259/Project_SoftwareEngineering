from sqlalchemy.orm import Session

from app.domain.employee import Employee, EmployeeRole


class EmployeeRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self._session.get(Employee, employee_id)

    def get_by_email(self, email: str) -> Employee | None:
        return (
            self._session.query(Employee)
            .filter_by(_email=email.strip())
            .first()
        )

    def get_by_role(self, role: EmployeeRole) -> list[Employee]:
        return (
            self._session.query(Employee)
            .filter_by(_role=role.value)
            .all()
        )

    def get_all(self) -> list[Employee]:
        return self._session.query(Employee).all()

    def save(self, employee: Employee) -> None:
        self._session.add(employee)

    def delete(self, employee: Employee) -> None:
        self._session.delete(employee)