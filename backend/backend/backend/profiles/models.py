import enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Column, Enum, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.users.models import UserDB


class ProfileBase(SQLModel):
    name: str


class ProfileDB(ProfileBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    accesses: list["ProfileAccessDB"] = Relationship(back_populates="profile")


class ProfileAccessType(enum.Enum):
    read = "R"
    write = "W"
    own = "O"


class ProfileAccessBase(SQLModel):
    profile_id: int = Field(foreign_key="profiledb.id", primary_key=True)
    user_id: int = Field(foreign_key="userdb.id", primary_key=True)
    access: ProfileAccessType = Field(
        sa_column=Column(Enum(ProfileAccessType), nullable=False)
    )


class ProfileAccessDB(ProfileAccessBase, table=True):
    profile: ProfileDB = Relationship(back_populates="accesses")
    user: "UserDB" = Relationship(back_populates="profile_accesses")
