from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.repositories.base import Base

from config import MAX_NAME_LENGTH, MAX_ROLE_LENGTH
from config import MAX_STREET_NAME_LENGTH, MAX_STREET_NUMBER_LENGTH, MAX_POSTAL_CODE_LENGTH, MAX_CITY_LENGTH, MAX_COUNTRY_LENGTH
from config import MAX_PHONE_NUMBER_LENGTH, MAX_EMAIL_ADDRESS_LENGTH,MAX_CUSTOMER_NOTES_LENGTH

#FIRST_NAME, LAST_NAME, ROLE, EMAIL, ID

class EmployeeRecord(Base):
    __tablename__= "employee"
id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
first_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
last_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
role: Mapped[str] = mapped_column(String(MAX_ROLE_LENGTH),nullable=False)
email: Mapped[str] = mapped_column(String(MAX_EMAIL_ADDRESS_LENGTH), nullable=False, unique=True)
phone: Mapped[str] = mapped_column(String(MAX_PHONE_NUMBER_LENGTH), nullable=False)