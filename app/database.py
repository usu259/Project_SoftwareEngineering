from sqlalchemy import create_engine

from app.repositories.base import Base

# Import all mapping modules so their tables register on Base.metadata.
from app.model import customer_mapping  # noqa: F401
from app.model import employee_mapping  # noqa: F401
from app.model import invoice_mapping  # noqa: F401
from app.model import work_report_mapping  # noqa: F401
from app.model import position_mapping  # noqa: F401


DATABASE_URL = "sqlite:///billing.db"
engine = create_engine(DATABASE_URL, echo=False, future=True)


def init_db() -> None:
    Base.metadata.create_all(engine)
