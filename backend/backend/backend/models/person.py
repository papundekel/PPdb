from datetime import date
from typing import Optional

from pydantic import validator
from sqlmodel import Field, SQLModel


class PersonBase(SQLModel):
    first_name: str
    last_name: str
    birthday: Optional[date] = None

    @validator("first_name")
    def validate_first_name(cls, first_name_value: str) -> str:
        if first_name_value == "":
            raise ValueError("First name must not be empty")
        return first_name_value

    @validator("last_name")
    def validate_last_name(cls, last_name_value: str) -> str:
        if last_name_value == "":
            raise ValueError("Last name must not be empty")
        return last_name_value


class PersonDB(PersonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
