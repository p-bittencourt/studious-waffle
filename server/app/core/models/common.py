"""Common models shared across multiple modules"""

from typing import Optional
from sqlmodel import SQLModel


class LocationBase(SQLModel):
    """Location auxiliary data structure"""

    type: str  # the type could be something like point of sale, warehouse for the vendor | house or office for the shopper, for instance
    street: str
    number: str
    complement: Optional[str] = None
    zip_code: str
    city: str
    state: str
    country: str


# For database storage as JSON
class Location(LocationBase):
    """For db storage as JSON"""

    pass
