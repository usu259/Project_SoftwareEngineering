from datetime import date
from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import Session
from app.database import engine
from app.service.work_report_service import WorkReportService
from app.service.customer_service import CustomerService
from app.service.employee_service import EmployeeService
from app.domain.exceptions import DomainError

work_report_bp = Blueprint("work_reports", __name__, url_prefix="/work-reports")


@work_report_bp.route("/", methods=["GET"])
def list_work_reports():
    with Session(engine) as session:
        service = WorkReportService(session)
        work_reports = service.get_all_work_reports()
    return render_template("work_reports/list.html", work_reports=work_reports)


@work_report_bp.route("/new", methods=["GET", "POST"])
def create_work_report():
    if request.method == "POST":
        try:
            with Session(engine) as session:
                service = WorkReportService(session)
                service.create_work_report(
                    customer_id=int(request.form.get("customer_id")),
                    employee_id=int(request.form.get("employee_id")),
                    title=request.form.get("title"),
                    description=request.form.get("description"),
                    execution_date=date.fromisoformat(request.form.get("execution_date")),
                    notes=request.form.get("notes") or None,
                )
                session.commit()
            return redirect(url_for("work_reports.list_work_reports"))
        except (DomainError, ValueError, TypeError) as e:
            flash(str(e), "error")
    with Session(engine) as session:
        customers = CustomerService(session).get_all_customers()
        employees = EmployeeService(session).get_all_employees()
    return render_template(
        "work_reports/create.html", customers=customers, employees=employees
    )


@work_report_bp.route("/<int:work_report_id>", methods=["GET"])
def get_work_report(work_report_id: int):
    with Session(engine) as session:
        service = WorkReportService(session)
        work_report = service.get_work_report(work_report_id)
    return render_template("work_reports/detail.html", work_report=work_report)


@work_report_bp.route("/<int:work_report_id>/edit", methods=["GET", "POST"])
def edit_work_report(work_report_id: int):
    if request.method == "POST":
        try:
            with Session(engine) as session:
                WorkReportService(session).update_work_report(
                    work_report_id=work_report_id,
                    title=request.form.get("title"),
                    description=request.form.get("description"),
                    execution_date=date.fromisoformat(request.form.get("execution_date")),
                    notes=request.form.get("notes") or None,
                )
                session.commit()
            return redirect(url_for("work_reports.get_work_report", work_report_id=work_report_id))
        except (DomainError, ValueError, TypeError) as e:
            flash(str(e), "error")
    with Session(engine) as session:
        work_report = WorkReportService(session).get_work_report(work_report_id)
    return render_template("work_reports/edit.html", work_report=work_report)


@work_report_bp.route("/<int:work_report_id>/add-personnel", methods=["POST"])
def add_personnel_position(work_report_id: int):
    try:
        with Session(engine) as session:
            service = WorkReportService(session)
            service.add_personnel_position(
                work_report_id=work_report_id,
                hours=Decimal(request.form.get("hours")),
                hourly_rate=Decimal(request.form.get("hourly_rate")),
                description=request.form.get("description") or None,
            )
            session.commit()
    except (DomainError, ValueError, TypeError) as e:
        flash(str(e), "error")
    return redirect(url_for("work_reports.get_work_report", work_report_id=work_report_id))


@work_report_bp.route("/<int:work_report_id>/add-material", methods=["POST"])
def add_material_position(work_report_id: int):
    try:
        with Session(engine) as session:
            service = WorkReportService(session)
            service.add_material_position(
                work_report_id=work_report_id,
                quantity=Decimal(request.form.get("quantity")),
                unit_price=Decimal(request.form.get("unit_price")),
                description=request.form.get("description") or None,
            )
            session.commit()
    except (DomainError, ValueError, TypeError) as e:
        flash(str(e), "error")
    return redirect(url_for("work_reports.get_work_report", work_report_id=work_report_id))


@work_report_bp.route("/<int:work_report_id>/remove-position/<int:position_id>", methods=["POST"])
def remove_position(work_report_id: int, position_id: int):
    try:
        with Session(engine) as session:
            service = WorkReportService(session)
            service.remove_position(work_report_id, position_id)
            session.commit()
    except (DomainError, ValueError, TypeError) as e:
        flash(str(e), "error")
    return redirect(url_for("work_reports.get_work_report", work_report_id=work_report_id))
