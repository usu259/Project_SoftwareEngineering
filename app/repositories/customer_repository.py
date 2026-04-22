from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.customer import Customer
from app.domain.value_objects import Address
from app.repositories.mappings import customer_table


class CustomerRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, customer_id: int) -> Customer | None:
        row = self._session.execute(
            select(customer_table).where(customer_table.c.id == customer_id)
        ).fetchone()

        if row is None:
            return None

        return self._row_to_customer(row)

    def get_by_email(self, email: str) -> Customer | None:
        row = self._session.execute(
            select(customer_table).where(customer_table.c.email == email.strip())
        ).fetchone()

        if row is None:
            return None

        return self._row_to_customer(row)

    def get_all(self) -> list[Customer]:
        rows = self._session.execute(select(customer_table)).fetchall()
        return [self._row_to_customer(row) for row in rows]

    def save(self, customer: Customer) -> None:
        data = {
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "street": customer.address.street,
            "city": customer.address.city,
            "zip_code": customer.address.zip_code,
            "country": customer.address.country,
        }

        if customer.id is None:
            result = self._session.execute(
                customer_table.insert().values(**data)
            )
            customer._id = result.inserted_primary_key[0]
        else:
            self._session.execute(
                customer_table.update()
                .where(customer_table.c.id == customer.id)
                .values(**data)
            )

    def delete(self, customer: Customer) -> None:
        if customer.id is None:
            raise ValueError("Cannot delete a customer that has not been persisted")
        self._session.execute(
            customer_table.delete().where(customer_table.c.id == customer.id)
        )

    def _row_to_customer(self, row) -> Customer:
        address = Address(
            street=row.street,
            city=row.city,
            zip_code=row.zip_code,
            country=row.country,
        )
        return Customer(
            first_name=row.first_name,
            last_name=row.last_name,
            email=row.email,
            phone=row.phone,
            address=address,
            id=row.id,
        )