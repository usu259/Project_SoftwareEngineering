import sys
import os
from sqlalchemy import create_engine

from app.repositories.base import Base

# Import all mapping modules so their tables register on Base.metadata.
from app.model import customer_mapping  # noqa: F401
from app.model import employee_mapping  # noqa: F401
from app.model import invoice_mapping  # noqa: F401
from app.model import work_report_mapping  # noqa: F401
from app.model import position_mapping  # noqa: F401


def _db_path() -> str:
    if getattr(sys, "frozen", False):
        # Store database next to the exe so it persists across runs
        return os.path.join(os.path.dirname(sys.executable), "billing.db")
    # Dev: project root (two levels up from this file)
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "billing.db")


DATABASE_URL = f"sqlite:///{_db_path()}"
engine = create_engine(DATABASE_URL, echo=False, future=True)


def init_db() -> None:
    Base.metadata.create_all(engine)
