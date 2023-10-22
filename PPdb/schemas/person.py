from datetime import date
from typing import Optional

from sqlmodel import SQLModel

from PPdb.models.person import PersonBase


class PersonCreate(PersonBase):
    pass


class PersonRead(PersonBase):
    id: int


class PersonUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
