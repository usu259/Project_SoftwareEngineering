from decimal import Decimal
from datetime import date
from sqlalchemy.orm import Session
from app.domain.work_report import WorkReport
from app.domain.position import MaterialPosition, PersonnelPosition
from app.repositories.work_report_repository import WorkReportRepository


class WorkReportService:
    def __init__(self, session: Session):
        self._session = session
        self._repo = WorkReportRepository(session)

    def create_work_report(
        self,
        customer_id: int,
        employee_id: int,
        title: str,
        description: str,
        execution_date: date,
        notes: str | None = None,
    ) -> WorkReport:
        work_report = WorkReport(
            customer_id=customer_id,
            employee_id=employee_id,
            title=title,
            description=description,
            execution_date=execution_date,
            notes=notes,
        )
        self._repo.save(work_report)
        self._session.flush()
        return work_report

    def get_work_report(self, work_report_id: int) -> WorkReport:
        work_report = self._repo.get_by_id(work_report_id)
        if work_report is None:
            raise ValueError(f"WorkReport with id {work_report_id!r} not found")
        return work_report

    def get_all_work_reports(self) -> list[WorkReport]:
        return self._repo.get_all()

    def get_work_reports_by_customer(self, customer_id: int) -> list[WorkReport]:
        return self._repo.get_by_customer(customer_id)

    def get_unassigned_work_reports(self, customer_id: int) -> list[WorkReport]:
        return self._repo.get_unassigned(customer_id)

    # Position management
    def add_personnel_position(
        self,
        work_report_id: int,
        hours: Decimal,
        hourly_rate: Decimal,
        description: str | None = None,
    ) -> WorkReport:
        work_report = self.get_work_report(work_report_id)
        position = PersonnelPosition(
            hours=hours,
            hourly_rate=hourly_rate,
            description=description,
        )
        work_report.add_position(position)
        self._repo.save(work_report)
        return work_report

    def add_material_position(
        self,
        work_report_id: int,
        quantity: Decimal,
        unit_price: Decimal,
        description: str | None = None,
    ) -> WorkReport:
        work_report = self.get_work_report(work_report_id)
        position = MaterialPosition(
            quantity=quantity,
            unit_price=unit_price,
            description=description,
        )
        work_report.add_position(position)
        self._repo.save(work_report)
        return work_report

    def remove_position(
        self,
        work_report_id: int,
        position_id: int,
    ) -> WorkReport:
        work_report = self.get_work_report(work_report_id)
        work_report.remove_position(position_id)
        self._repo.save(work_report)
        return work_report