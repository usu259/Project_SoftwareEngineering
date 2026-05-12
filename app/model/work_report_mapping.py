from datetime import date
from sqlalchemy import String, Date, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.repositories.base import Base
from config import (
    MAX_WORK_REPORT_TITLE_LENGTH,
    MAX_WORK_REPORT_DESCRIPTION_LENGTH,
    MAX_WORK_REPORT_NOTES_LENGTH,
)


class WorkReportRecord(Base):
    __tablename__ = "work_reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    invoice_id: Mapped[int | None] = mapped_column(ForeignKey("invoices.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(MAX_WORK_REPORT_TITLE_LENGTH), nullable=False)
    description: Mapped[str] = mapped_column(String(MAX_WORK_REPORT_DESCRIPTION_LENGTH), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(MAX_WORK_REPORT_NOTES_LENGTH), nullable=True)
    execution_date: Mapped[date] = mapped_column(Date, nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    invoice_record: Mapped["InvoiceRecord"] = relationship(back_populates="work_report_records")
    personnel_position_records: Mapped[list["PersonnelPositionRecord"]] = relationship(
        back_populates="work_report_record", cascade="all, delete-orphan"
    )
    material_position_records: Mapped[list["MaterialPositionRecord"]] = relationship(
        back_populates="work_report_record", cascade="all, delete-orphan"
    )
