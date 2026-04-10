from dataclasses import dataclass

@dataclass(frozen=True)
class Address:
    """Represents a postal address as an immutable value object"""
    street: str
    city: str
    zip_code: str
    country: str


    