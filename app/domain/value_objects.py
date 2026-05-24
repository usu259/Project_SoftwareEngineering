from dataclasses import dataclass
from app.domain.validations import (
    _validate_street,
    _validate_city,
    _validate_zip_code,
    _validate_country,
)


@dataclass(frozen=True)
class Address:
    """Represents a postal address as an immutable value object."""
    street: str
    city: str
    zip_code: str
    country: str

    def __post_init__(self):
        object.__setattr__(self, "street", _validate_street(self.street))
        object.__setattr__(self, "city", _validate_city(self.city))
        object.__setattr__(self, "zip_code", _validate_zip_code(self.zip_code))
        object.__setattr__(self, "country", _validate_country(self.country))
