from datetime import date
from typing import Optional

from sqlmodel import SQLModel

from backend.persons.models import PersonBase


class PersonCreate(PersonBase):
    pass


class PersonRead(PersonBase):
    id: int


class PersonUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
