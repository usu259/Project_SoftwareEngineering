
import datetime
from abc import ABC, abstractmethod
from decimal import Decimal

class position(ABC):

    _MAX_NOTES_LENGTH = 1000
    
    def __init__(self, worker_id:int,
                 project_id:int,
                 stem_item_id: int,
                 work_date: datetime.date,
                 unit_price_at_entry: Decimal,
                 notes: str | None = None,
                 work_report_id: int | None = None,
                 id: int | None = None):
        

    @staticmethod
    def _validate_worker_id(value)
    

    @staticmethod
    def _validate_work_date(value: datetime.date) -> datetime.date:
        if value is None:
            raise ValueError("work_date cannot be empty")
        if not isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
            raise TypeError(f"fowrk_date must be a datetime.date, got {type(value).__name__}")
    
