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
