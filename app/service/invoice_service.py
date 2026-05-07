from sqlalchemy.orm import Session
from domain.invoice import Invoice, InvoiceStatus
from domain.work_report import WorkReport
from repositories.invoice_repository import InvoiceRepository
from repositories.work_report_repository import WorkReportRepository

class InvoiceService:
    def __init__(self, session: Session):
        self._session = session
        self._repo = InvoiceRepository(session)
        self._work_report_repo = WorkReportRepository(session)

    def create_invoice(
        self,
        customer_id: int,
        title: str,
        description: str,
        notes: str | None = None,
    ) -> Invoice:
        invoice = Invoice(
            customer_id=customer_id,
            title=title,
            description=description,
            notes=notes,
        )
        self._repo.save(invoice)
        self._session.flush()
        return invoice

    def get_invoice(self, invoice_id: int) -> Invoice:
        invoice = self._repo.get_by_id(invoice_id)
        if invoice is None:
            raise ValueError(f"Invoice with id {invoice_id!r} not found")
        return invoice

    def get_all_invoices(self) -> list[Invoice]:
        return self._repo.get_all()

    def get_invoices_by_customer(self, customer_id: int) -> list[Invoice]:
        return self._repo.get_by_customer(customer_id)

    def update_invoice_title(self, invoice_id: int, title: str) -> Invoice:
        invoice = self.get_invoice(invoice_id)
        invoice.change_title(title)
        self._repo.save(invoice)
        return invoice

    def update_invoice_description(self, invoice_id: int, description: str) -> Invoice:
        invoice = self.get_invoice(invoice_id)
        invoice.change_description(description)
        self._repo.save(invoice)
        return invoice

    def update_invoice_notes(self, invoice_id: int, notes: str) -> Invoice:
        invoice = self.get_invoice(invoice_id)
        invoice.change_notes(notes)
        self._repo.save(invoice)
        return invoice

    def add_work_report(self, invoice_id: int, work_report_id: int) -> Invoice:
        invoice = self.get_invoice(invoice_id)
        work_report = self._work_report_repo.get_by_id(work_report_id)
        if work_report is None:
            raise ValueError(f"WorkReport with id {work_report_id!r} not found")
        invoice.add_work_report(work_report)
        self._repo.save(invoice)
        return invoice

    def remove_work_report(self, invoice_id: int, work_report_id: int) -> Invoice:
        invoice = self.get_invoice(invoice_id)
        invoice.remove_work_report(work_report_id)
        self._repo.save(invoice)
        return invoice

    def send_invoice(self, invoice_id: int) -> Invoice:
        invoice = self.get_invoice(invoice_id)
        invoice.change_status(InvoiceStatus.SENT)
        self._repo.save(invoice)
        return invoice

    def mark_invoice_paid(self, invoice_id: int) -> Invoice:
        invoice = self.get_invoice(invoice_id)
        invoice.change_status(InvoiceStatus.PAID)
        self._repo.save(invoice)
        return invoice

    def delete_invoice(self, invoice_id: int) -> None:
        invoice = self.get_invoice(invoice_id)
        invoice.mark_deleted()
        self._repo.save(invoice)