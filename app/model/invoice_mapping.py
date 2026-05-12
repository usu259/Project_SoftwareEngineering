from datetime import date
from sqlalchemy import String, Date, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.repositories.base import Base
from config import (
    MAX_INVOICE_TITLE_LENGTH,
    MAX_INVOICE_DESCRIPTION_LENGTH,
    MAX_INVOICE_NOTES_LENGTH,
)


class InvoiceRecord(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(MAX_INVOICE_TITLE_LENGTH), nullable=False)
    description: Mapped[str] = mapped_column(String(MAX_INVOICE_DESCRIPTION_LENGTH), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(MAX_INVOICE_NOTES_LENGTH), nullable=True)
    creation_date: Mapped[date] = mapped_column(Date, nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    customer_record: Mapped["CustomerRecord"] = relationship(back_populates="invoice_records")
    work_report_records: Mapped[list["WorkReportRecord"]] = relationship(back_populates="invoice_record")
