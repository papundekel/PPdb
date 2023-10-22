from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class PersonBase(SQLModel):
    first_name: str
    last_name: str
    birthday: Optional[date] = None


class PersonDB(PersonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
