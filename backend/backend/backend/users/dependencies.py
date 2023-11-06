from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import joinedload
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from backend.database import get_session
from backend.users import oauth2_scheme
from backend.users.models import TokenDB, UserDB
from backend.utils import get_not_id


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    if token is None:
        return None

    token_db = await get_not_id(
        session, TokenDB, TokenDB.token, token, joinedload(TokenDB.user)
    )

    if token_db is None:
        return None

    user = token_db.user

    return user


async def require_login(user: Annotated[UserDB, Depends(get_current_user)]):
    if user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated."
        )

    return user
