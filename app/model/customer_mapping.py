from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.repositories.base import Base

from config import (
    MAX_NAME_LENGTH,
    MAX_STREET_NAME_LENGTH,
    MAX_POSTAL_CODE_LENGTH,
    MAX_CITY_LENGTH,
    MAX_COUNTRY_LENGTH,
    MAX_PHONE_NUMBER_LENGTH,
    MAX_EMAIL_ADDRESS_LENGTH,
)


class CustomerRecord(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    last_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    email: Mapped[str] = mapped_column(String(MAX_EMAIL_ADDRESS_LENGTH), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(MAX_PHONE_NUMBER_LENGTH), nullable=False)
    street: Mapped[str] = mapped_column(String(MAX_STREET_NAME_LENGTH), nullable=False)
    city: Mapped[str] = mapped_column(String(MAX_CITY_LENGTH), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(MAX_POSTAL_CODE_LENGTH), nullable=False)
    country: Mapped[str] = mapped_column(String(MAX_COUNTRY_LENGTH), nullable=False)

    invoice_records: Mapped[list["InvoiceRecord"]] = relationship(
        back_populates="customer_record"
    )
