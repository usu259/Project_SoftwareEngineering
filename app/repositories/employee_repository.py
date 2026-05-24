from sqlalchemy.orm import Session

from app.domain.employee import Employee, EmployeeRole
from app.model.employee_mapping import EmployeeRecord


class EmployeeRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, employee_id: int) -> Employee | None:
        record = self._session.get(EmployeeRecord, employee_id)
        if record is None:
            return None
        return self._to_domain(record)

    def get_by_email(self, email: str) -> Employee | None:
        record = (
            self._session.query(EmployeeRecord)
            .filter_by(email=email.strip())
            .first()
        )
        if record is None:
            return None
        return self._to_domain(record)

    def get_by_role(self, role: EmployeeRole) -> list[Employee]:
        records = (
            self._session.query(EmployeeRecord)
            .filter_by(role=role.value)
            .all()
        )
        return [self._to_domain(r) for r in records]

    def get_all(self) -> list[Employee]:
        records = self._session.query(EmployeeRecord).all()
        return [self._to_domain(r) for r in records]

    def save(self, employee: Employee) -> None:
        if employee.id is None:
            record = self._to_model(employee)
            self._session.add(record)
            self._session.flush()
            employee._id = record.id
        else:
            record = self._session.get(EmployeeRecord, employee.id)
            if record is None:
                raise ValueError(f"Employee {employee.id} not found")
            self._update_record(record, employee)

    def delete(self, employee: Employee) -> None:
        if employee.id is None:
            raise ValueError("Cannot delete an employee that has not been persisted")
        record = self._session.get(EmployeeRecord, employee.id)
        if record is not None:
            self._session.delete(record)

    def _to_model(self, employee: Employee) -> EmployeeRecord:
        return EmployeeRecord(
            id=employee.id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            phone=employee.phone,
            role=employee.role.value,
        )

    def _to_domain(self, record: EmployeeRecord) -> Employee:
        return Employee(
            id=record.id,
            first_name=record.first_name,
            last_name=record.last_name,
            email=record.email,
            phone=record.phone,
            role=EmployeeRole(record.role),
        )

    def _update_record(self, record: EmployeeRecord, employee: Employee) -> None:
        record.first_name = employee.first_name
        record.last_name = employee.last_name
        record.email = employee.email
        record.phone = employee.phone
        record.role = employee.role.value
