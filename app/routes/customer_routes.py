from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import Session
from app.database import engine
from app.service.customer_service import CustomerService
from app.domain.value_objects import Address
from app.domain.exceptions import DomainError

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customer_bp.route("/", methods=["GET"])
def list_customers():
    with Session(engine) as session:
        service = CustomerService(session)
        customers = service.get_all_customers()
    return render_template("customers/list.html", customers=customers)


@customer_bp.route("/new", methods=["GET", "POST"])
def create_customer():
    if request.method == "POST":
        try:
            with Session(engine) as session:
                service = CustomerService(session)
                service.create_customer(
                    first_name=request.form.get("first_name"),
                    last_name=request.form.get("last_name"),
                    email=request.form.get("email"),
                    phone=request.form.get("phone"),
                    address=Address(
                        street=request.form.get("street"),
                        city=request.form.get("city"),
                        zip_code=request.form.get("zip_code"),
                        country=request.form.get("country"),
                    ),
                )
                session.commit()
            return redirect(url_for("customers.list_customers"))
        except (DomainError, ValueError, TypeError) as e:
            flash(str(e), "error")
    return render_template("customers/create.html")


@customer_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id: int):
    with Session(engine) as session:
        service = CustomerService(session)
        customer = service.get_customer(customer_id)
    return render_template("customers/detail.html", customer=customer)


@customer_bp.route("/<int:customer_id>/edit", methods=["GET", "POST"])
def edit_customer(customer_id: int):
    if request.method == "POST":
        try:
            with Session(engine) as session:
                service = CustomerService(session)
                service.update_customer_name(
                    customer_id=customer_id,
                    first_name=request.form.get("first_name"),
                    last_name=request.form.get("last_name"),
                )
                service.update_customer_contact(
                    customer_id=customer_id,
                    email=request.form.get("email"),
                    phone=request.form.get("phone"),
                )
                service.update_customer_address(
                    customer_id=customer_id,
                    address=Address(
                        street=request.form.get("street"),
                        city=request.form.get("city"),
                        zip_code=request.form.get("zip_code"),
                        country=request.form.get("country"),
                    ),
                )
                session.commit()
            return redirect(url_for("customers.get_customer", customer_id=customer_id))
        except (DomainError, ValueError, TypeError) as e:
            flash(str(e), "error")
    with Session(engine) as session:
        service = CustomerService(session)
        customer = service.get_customer(customer_id)
    return render_template("customers/edit.html", customer=customer)
