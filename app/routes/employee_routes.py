from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import Session
from app.database import engine
from app.service.employee_service import EmployeeService
from app.domain.employee import EmployeeRole
from app.domain.exceptions import DomainError

employee_bp = Blueprint("employees", __name__, url_prefix="/employees")


@employee_bp.route("/", methods=["GET"])
def list_employees():
    with Session(engine) as session:
        employees = EmployeeService(session).get_all_employees()
    return render_template("employees/list.html", employees=employees)


@employee_bp.route("/new", methods=["GET", "POST"])
def create_employee():
    if request.method == "POST":
        try:
            with Session(engine) as session:
                EmployeeService(session).create_employee(
                    first_name=request.form.get("first_name"),
                    last_name=request.form.get("last_name"),
                    email=request.form.get("email"),
                    phone=request.form.get("phone"),
                    role=EmployeeRole(request.form.get("role")),
                )
                session.commit()
            return redirect(url_for("employees.list_employees"))
        except (DomainError, ValueError, TypeError) as e:
            flash(str(e), "error")
    return render_template("employees/create.html", roles=list(EmployeeRole))


@employee_bp.route("/<int:employee_id>", methods=["GET"])
def get_employee(employee_id: int):
    with Session(engine) as session:
        employee = EmployeeService(session).get_employee(employee_id)
    return render_template("employees/detail.html", employee=employee)


@employee_bp.route("/<int:employee_id>/edit", methods=["GET", "POST"])
def edit_employee(employee_id: int):
    if request.method == "POST":
        try:
            with Session(engine) as session:
                service = EmployeeService(session)
                service.update_employee_name(
                    employee_id,
                    first_name=request.form.get("first_name"),
                    last_name=request.form.get("last_name"),
                )
                service.update_employee_email(employee_id, request.form.get("email"))
                service.update_employee_role(employee_id, EmployeeRole(request.form.get("role")))
                session.commit()
            return redirect(url_for("employees.get_employee", employee_id=employee_id))
        except (DomainError, ValueError, TypeError) as e:
            flash(str(e), "error")
    with Session(engine) as session:
        employee = EmployeeService(session).get_employee(employee_id)
    return render_template("employees/edit.html", employee=employee, roles=list(EmployeeRole))


@employee_bp.route("/<int:employee_id>/delete", methods=["POST"])
def delete_employee(employee_id: int):
    try:
        with Session(engine) as session:
            EmployeeService(session).delete_employee(employee_id)
            session.commit()
    except (DomainError, ValueError, TypeError) as e:
        flash(str(e), "error")
    return redirect(url_for("employees.list_employees"))
