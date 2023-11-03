from sys import stderr
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import joinedload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.database import get_session
from backend.users import oauth2_scheme
from backend.users.models import TokenDB
from backend.utils import select_all_list


async def get_current_user(
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    print(f"{token=}", file=stderr)
    print(await select_all_list(session, TokenDB), file=stderr)

    token_db = (
        await session.exec(
            select(TokenDB)
            .where(TokenDB.token == token)
            .options(joinedload(TokenDB.user))
        )
    ).first()

    if token_db is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = token_db.user

    return user
