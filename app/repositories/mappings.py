from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import registry

from app.domain.employee import Employee, EmployeeRole

metadata = MetaData()
mapper_registry = registry()

customer_table = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String(100), nullable=False),
    Column("last_name", String(100), nullable=False),
    Column("email", String(255), nullable=False, unique=True),
    Column("phone", String(50), nullable=False),
    Column("street", String(255), nullable=False),
    Column("city", String(100), nullable=False),
    Column("zip_code", String(20), nullable=False),
    Column("country", String(100), nullable=False),
)

employee_table = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String(100), nullable=False),
    Column("last_name", String(100), nullable=False),
    Column("email", String(255), nullable=False, unique=True),
    Column("role", String(50), nullable=False),
)


def configure_mappers():
    mapper_registry.map_imperatively(
        Employee,
        employee_table,
        properties={
            "_id": employee_table.c.id,
            "_first_name": employee_table.c.first_name,
            "_last_name": employee_table.c.last_name,
            "_email": employee_table.c.email,
            "_role": employee_table.c.role,
        },
    )