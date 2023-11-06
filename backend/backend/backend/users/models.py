from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.profiles.models import ProfileAccessDB


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)


class UserDB(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    tokens: List["TokenDB"] = Relationship(back_populates="user")
    profile_accesses: List["ProfileAccessDB"] = Relationship(back_populates="user")


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
    email: EmailStr = Field(primary_key=True)


class RegistrationApprovalDB(RegistrationApproval, table=True):
    pass
