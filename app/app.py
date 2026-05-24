import sys
import os
from flask import Flask, render_template

from app.database import init_db
from app.routes.customer_routes import customer_bp
from app.routes.work_report_routes import work_report_bp
from app.routes.invoice_routes import invoice_bp
from app.routes.employee_routes import employee_bp


def _resource_path(relative_path: str) -> str:
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=_resource_path("templates"),
        static_folder=_resource_path("static"),
    )
    app.secret_key = "dev-secret-change-me"

    init_db()

    app.register_blueprint(customer_bp)
    app.register_blueprint(work_report_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(employee_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
