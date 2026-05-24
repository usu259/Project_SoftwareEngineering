from decimal import Decimal
from sqlalchemy.orm import Session
from app.domain.work_report import WorkReport
from app.domain.position import PersonnelPosition, MaterialPosition
from app.model.work_report_mapping import WorkReportRecord
from app.model.position_mapping import PersonnelPositionRecord, MaterialPositionRecord


class WorkReportRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, work_report_id: int) -> WorkReport | None:
        record = self._session.get(WorkReportRecord, work_report_id)
        if record is None:
            return None
        return self._to_domain(record)

    def get_all(self) -> list[WorkReport]:
        records = self._session.query(WorkReportRecord).all()
        return [self._to_domain(r) for r in records]

    def get_by_customer(self, customer_id: int) -> list[WorkReport]:
        records = self._session.query(WorkReportRecord).filter_by(customer_id=customer_id).all()
        return [self._to_domain(r) for r in records]

    def get_unassigned(self, customer_id: int) -> list[WorkReport]:
        records = (
            self._session.query(WorkReportRecord)
            .filter_by(customer_id=customer_id, invoice_id=None)
            .all()
        )
        return [self._to_domain(r) for r in records]

    def save(self, work_report: WorkReport) -> None:
        if work_report.id is None:
            record = self._to_model(work_report)
            self._session.add(record)
            self._session.flush()
            work_report._id = record.id
        else:
            record = self._session.get(WorkReportRecord, work_report.id)
            if record is None:
                raise ValueError(f"WorkReport {work_report.id} not found")
            self._update_record(record, work_report)

    def _to_model(self, work_report: WorkReport) -> WorkReportRecord:
        record = WorkReportRecord(
            customer_id=work_report.customer_id,
            employee_id=work_report.employee_id,
            invoice_id=work_report.invoice_id,
            title=work_report.title,
            description=work_report.description,
            notes=work_report.notes,
            execution_date=work_report.execution_date,
            deleted=False,
        )
        for p in work_report.positions:
            if isinstance(p, PersonnelPosition):
                record.personnel_position_records.append(
                    PersonnelPositionRecord(
                        description=p.description,
                        hours=p.hours,
                        hourly_rate=p.hourly_rate,
                    )
                )
            elif isinstance(p, MaterialPosition):
                record.material_position_records.append(
                    MaterialPositionRecord(
                        description=p.description,
                        quantity=p.quantity,
                        unit_price=p.unit_price,
                    )
                )
        return record

    def _to_domain(self, record: WorkReportRecord) -> WorkReport:
        positions = (
            [self._personnel_to_domain(p) for p in record.personnel_position_records]
            + [self._material_to_domain(m) for m in record.material_position_records]
        )
        return WorkReport(
            id=record.id,
            customer_id=record.customer_id,
            employee_id=record.employee_id,
            invoice_id=record.invoice_id,
            title=record.title,
            description=record.description,
            notes=record.notes,
            execution_date=record.execution_date,
            positions=positions,
        )

    def _update_record(self, record: WorkReportRecord, work_report: WorkReport) -> None:
        record.customer_id = work_report.customer_id
        record.employee_id = work_report.employee_id
        record.invoice_id = work_report.invoice_id
        record.title = work_report.title
        record.description = work_report.description
        record.notes = work_report.notes
        record.execution_date = work_report.execution_date

        record.personnel_position_records.clear()
        record.material_position_records.clear()
        for p in work_report.positions:
            if isinstance(p, PersonnelPosition):
                record.personnel_position_records.append(
                    PersonnelPositionRecord(
                        description=p.description,
                        hours=p.hours,
                        hourly_rate=p.hourly_rate,
                    )
                )
            elif isinstance(p, MaterialPosition):
                record.material_position_records.append(
                    MaterialPositionRecord(
                        description=p.description,
                        quantity=p.quantity,
                        unit_price=p.unit_price,
                    )
                )

    def _personnel_to_domain(self, record: PersonnelPositionRecord) -> PersonnelPosition:
        return PersonnelPosition(
            id=record.id,
            hours=Decimal(record.hours),
            hourly_rate=Decimal(record.hourly_rate),
            description=record.description,
        )

    def _material_to_domain(self, record: MaterialPositionRecord) -> MaterialPosition:
        return MaterialPosition(
            id=record.id,
            quantity=Decimal(record.quantity),
            unit_price=Decimal(record.unit_price),
            description=record.description,
        )
