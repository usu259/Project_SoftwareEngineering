from sqlalchemy.orm import Session
from app.domain.customer import Customer
from app.domain.value_objects import Address
from app.repositories.customer_repository import CustomerRepository


class CustomerService:
    def __init__(self, session: Session):
        self._session = session
        self._repo = CustomerRepository(session)

    def create_customer(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: Address,
    ) -> Customer:
        if self._repo.get_by_email(email) is not None:
            raise ValueError(f"Email {email!r} is already in use")
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
        )
        self._repo.save(customer)
        self._session.flush()  # fill customer_id without commit
        return customer

    def get_customer(self, customer_id: int) -> Customer:
        customer = self._repo.get_by_id(customer_id)
        if customer is None:
            raise ValueError(f"Customer with id {customer_id!r} not found")
        return customer

    def get_all_customers(self) -> list[Customer]:
        return self._repo.get_all()

    def update_customer_contact(
        self,
        customer_id: int,
        email: str | None = None,
        phone: str | None = None,
    ) -> Customer:
        customer = self.get_customer(customer_id)

        if email is not None and email != customer.email:
            if self._repo.get_by_email(email) is not None:
                raise ValueError(f"Email {email!r} is already in use")

        customer.update_contact(email=email, phone=phone)
        return customer

    def update_customer_name(
        self,
        customer_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> Customer:
        customer = self.get_customer(customer_id)
        customer.update_name(first_name=first_name, last_name=last_name)
        return customer

    def update_customer_address(
        self, customer_id: int, address: Address
    ) -> Customer:
        customer = self.get_customer(customer_id)
        customer.update_address(address)
        return customer

 #   def delete_customer(self, customer_id: int) -> None:
#      customer = self.get_customer(customer_id)
 #       self._repo.delete(customer)