import email
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel

from backend.users.models import UserBase


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
