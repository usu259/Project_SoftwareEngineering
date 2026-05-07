from decimal import Decimal
from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.repositories.base import Base


class PersonnelPositionRecord(Base):
    __tablename__ = "personnel_positions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    work_report_id: Mapped[int] = mapped_column(
        ForeignKey("work_reports.id"), nullable=False
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hours: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    hourly_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    work_report_record: Mapped["WorkReportRecord"] = relationship(
        back_populates="personnel_position_records"
    )


class MaterialPositionRecord(Base):
    __tablename__ = "material_positions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    work_report_id: Mapped[int] = mapped_column(
        ForeignKey("work_reports.id"), nullable=False
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    work_report_record: Mapped["WorkReportRecord"] = relationship(
        back_populates="material_position_records"
    )
