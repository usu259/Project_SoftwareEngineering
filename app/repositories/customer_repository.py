from sqlalchemy.orm import Session

from app.domain.customer import Customer
from app.domain.value_objects import Address
from app.model.customer_mapping import CustomerRecord

class CustomerRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, customer_id: int) -> Customer | None:
        record = self._session.get(CustomerRecord, customer_id)
        if record is None:
            return None
        return self._to_domain(record)

    def get_by_email(self, email: str) -> Customer | None:
        record = self._session.query(CustomerRecord).filter_by(email=email.strip()).first()
        if record is None:
            return None
        return self._to_domain(record)

    def get_all(self) -> list[Customer]:
        records = self._session.query(CustomerRecord).all()
        return [self._to_domain(r) for r in records]

    def save(self, customer: Customer) -> None:
        if customer.id is None:
            record = self._to_model(customer)
            self._session.add(record)
            self._session.flush()         # genera l'id senza commit
            customer._id = record.id
        else:
            record = self._session.get(CustomerRecord, customer.id)
            if record is None:
                raise ValueError(f"Customer {customer.id} not found")
            self._update_record(record, customer)

    def delete(self, customer: Customer) -> None:
        if customer.id is None:
            raise ValueError("Cannot delete a customer that has not been persisted")
        record = self._session.get(CustomerRecord, customer.id)
        if record is not None:
            self._session.delete(record)

    def _to_model(self, customer: Customer) -> CustomerRecord:
        return CustomerRecord(
            id=customer.id,
            first_name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email,
            phone=customer.phone,
            street=customer.address.street,
            city=customer.address.city,
            zip_code=customer.address.zip_code,
            country=customer.address.country,
        )

    def _to_domain(self, record: CustomerRecord) -> Customer:
        return Customer(
            id=record.id,
            first_name=record.first_name,
            last_name=record.last_name,
            email=record.email,
            phone=record.phone,
            address=Address(
                street=record.street,
                city=record.city,
                zip_code=record.zip_code,
                country=record.country,
            ),
        )

    def _update_record(self, record: CustomerRecord, customer: Customer) -> None:
        record.first_name = customer.first_name
        record.last_name = customer.last_name
        record.email = customer.email
        record.phone = customer.phone
        record.street = customer.address.street
        record.city = customer.address.city
        record.zip_code = customer.address.zip_code
        record.country = customer.address.country
