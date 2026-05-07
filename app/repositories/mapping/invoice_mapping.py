from datetime import date
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from repositories.base import Base
from repositories.mapping.customer_mapping import CustomerRecord
from repositories.mapping.work_report_mapping import WorkReportRecord
from config import MAX_INVOICE_TITLE_LENGTH, MAX_INVOICE_DESCRIPTION_LENGTH, MAX_INVOICE_NOTES_LENGTH
from domain.invoice import Invoice, InvoiceStatus

class InvoiceRecord(Base):
    __tablename__ = "invoice"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    status: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(String(MAX_INVOICE_TITLE_LENGTH))
    description: Mapped[str] = mapped_column(String(MAX_INVOICE_DESCRIPTION_LENGTH))
    notes: Mapped[str | None] = mapped_column(String(MAX_INVOICE_NOTES_LENGTH), nullable=True)
    creation_date: Mapped[date] = mapped_column(Date)
    deleted: Mapped[bool]

    customer_record: Mapped["CustomerRecord"] = relationship(back_populates="invoice_records")
    work_report_records: Mapped[list["WorkReportRecord"]] = relationship(back_populates="invoice_record")
