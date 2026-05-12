from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import Session
from app.database import engine
from app.service.invoice_service import InvoiceService
from app.service.customer_service import CustomerService
from app.domain.exceptions import DomainError

invoice_bp = Blueprint("invoices", __name__, url_prefix="/invoices")


@invoice_bp.route("/", methods=["GET"])
def list_invoices():
    with Session(engine) as session:
        service = InvoiceService(session)
        invoices = service.get_all_invoices()
    return render_template("invoices/list.html", invoices=invoices)


@invoice_bp.route("/new", methods=["GET", "POST"])
def create_invoice():
    if request.method == "POST":
        try:
            with Session(engine) as session:
                service = InvoiceService(session)
                service.create_invoice(
                    customer_id=int(request.form.get("customer_id")),
                    title=request.form.get("title"),
                    description=request.form.get("description"),
                    notes=request.form.get("notes") or None,
                )
                session.commit()
            return redirect(url_for("invoices.list_invoices"))
        except (DomainError, ValueError, TypeError) as e:
            flash(str(e), "error")
    with Session(engine) as session:
        customers = CustomerService(session).get_all_customers()
    return render_template("invoices/create.html", customers=customers)


@invoice_bp.route("/<int:invoice_id>", methods=["GET"])
def get_invoice(invoice_id: int):
    with Session(engine) as session:
        service = InvoiceService(session)
        invoice = service.get_invoice(invoice_id)
    return render_template("invoices/detail.html", invoice=invoice)


@invoice_bp.route("/<int:invoice_id>/send", methods=["POST"])
def send_invoice(invoice_id: int):
    try:
        with Session(engine) as session:
            service = InvoiceService(session)
            service.send_invoice(invoice_id)
            session.commit()
    except (DomainError, ValueError, TypeError) as e:
        flash(str(e), "error")
    return redirect(url_for("invoices.get_invoice", invoice_id=invoice_id))


@invoice_bp.route("/<int:invoice_id>/pay", methods=["POST"])
def pay_invoice(invoice_id: int):
    try:
        with Session(engine) as session:
            service = InvoiceService(session)
            service.mark_invoice_paid(invoice_id)
            session.commit()
    except (DomainError, ValueError, TypeError) as e:
        flash(str(e), "error")
    return redirect(url_for("invoices.get_invoice", invoice_id=invoice_id))
