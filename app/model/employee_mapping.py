from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.repositories.base import Base

from config import (
    MAX_NAME_LENGTH,
    MAX_ROLE_LENGTH,
    MAX_PHONE_NUMBER_LENGTH,
    MAX_EMAIL_ADDRESS_LENGTH,
)


class EmployeeRecord(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    last_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    role: Mapped[str] = mapped_column(String(MAX_ROLE_LENGTH), nullable=False)
    email: Mapped[str] = mapped_column(String(MAX_EMAIL_ADDRESS_LENGTH), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(MAX_PHONE_NUMBER_LENGTH), nullable=False)
