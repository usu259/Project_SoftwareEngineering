from sqlalchemy.orm import Session
from domain.invoice import Invoice, InvoiceStatus
from domain.work_report import WorkReport
from repositories.mapping.invoice_mapping import InvoiceRecord
from repositories.mapping.work_report_mapping import WorkReportRecord


class InvoiceRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, invoice_id: int) -> Invoice | None:
        record = self._session.get(InvoiceRecord, invoice_id)
        if record is None:
            return None
        return self._to_domain(record)

    def get_all(self) -> list[Invoice]:
        records = self._session.query(InvoiceRecord).all()
        return [self._to_domain(r) for r in records]

    def get_by_customer(self, customer_id: int) -> list[Invoice]:
        records = self._session.query(InvoiceRecord).filter_by(customer_id=customer_id).all()
        return [self._to_domain(r) for r in records]

    def save(self, invoice: Invoice) -> None:
        if invoice.id is None:
            record = self._to_model(invoice)
            self._session.add(record)
            self._session.flush()
            invoice._id = record.id
        else:
            record = self._session.get(InvoiceRecord, invoice.id)
            if record is None:
                raise ValueError(f"Invoice {invoice.id} not found")
            self._update_record(record, invoice)

    def _to_model(self, invoice: Invoice) -> InvoiceRecord:
        return InvoiceRecord(
            customer_id=invoice.customer_id,
            status=invoice.status.name,
            title=invoice.title,
            description=invoice.description,
            notes=invoice.notes,
            creation_date=invoice.creation_date,
            deleted=invoice.deleted,
        )

    def _to_domain(self, record: InvoiceRecord) -> Invoice:
        return Invoice(
            id=record.id,
            customer_id=record.customer_id,
            status=InvoiceStatus[record.status],
            title=record.title,
            description=record.description,
            notes=record.notes,
            creation_date=record.creation_date,
            deleted=record.deleted,
            work_reports=[self._work_report_to_domain(wr) for wr in record.work_report_records]
        )

    def _update_record(self, record: InvoiceRecord, invoice: Invoice) -> None:
        record.customer_id = invoice.customer_id
        record.status = invoice.status.name
        record.title = invoice.title
        record.description = invoice.description
        record.notes = invoice.notes
        record.creation_date = invoice.creation_date
        record.deleted = invoice.deleted

    def _work_report_to_domain(self, record: WorkReportRecord) -> WorkReport:
        return WorkReport(
            id=record.id,
            customer_id=record.customer_id,
            employee_id=record.employee_id,
            title=record.title,
            description=record.description,
            notes=record.notes,
            execution_date=record.execution_date,
            invoice_id=record.invoice_id,
        )