from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr
from sqlmodel import AutoString, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.profiles.models import ProfileAccessDB


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, sa_type=AutoString)


class UserDB(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    tokens: list["TokenDB"] = Relationship(back_populates="user")
    profile_accesses: list["ProfileAccessDB"] = Relationship(back_populates="user")


class TokenBase(SQLModel):
    token: str = Field(primary_key=True)
    user_id: int = Field(foreign_key="userdb.id")
    expires: datetime


class TokenDB(TokenBase, table=True):
    user: UserDB = Relationship(back_populates="tokens")


class AccessToken(SQLModel):
    access_token: str
    token_type: str


class RegistrationApproval(SQLModel):
    email: EmailStr = Field(primary_key=True, sa_type=AutoString)


class RegistrationApprovalDB(RegistrationApproval, table=True):
    pass
