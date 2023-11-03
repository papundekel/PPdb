from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.database import get_session
from backend.users import oauth2_scheme, pwd_context
from backend.users.dependencies import get_current_user
from backend.users.models import TokenDB, UserDB
from backend.users.schemas import UserCreate, UserRead, UserUpdate
from backend.utils import (
    add_commit_refresh,
    delete_commit,
    get_or_404,
    select_all_list,
    update_instance,
)

router = APIRouter(tags=["users"], prefix="/users")


@router.post("/login")
async def login(
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    form: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    email = form.username
    password = form.password

    user_db = (await session.exec(select(UserDB).where(UserDB.email == email))).first()

    exception = HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if user_db is None:
        raise exception

    password_matches = pwd_context.verify(password, user_db.hashed_password)

    if not password_matches:
        raise exception

    token_db = TokenDB(
        token=token_urlsafe(), expires=datetime.now() + timedelta(days=2), user=user_db
    )  # type: ignore

    await add_commit_refresh(session, token_db)

    return {"access_token": token_db.token, "token_type": "bearer"}


@router.delete("/login")
async def logout(
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)]
):
    token_db = (
        await session.exec(select(TokenDB).where(TokenDB.token == token))
    ).first()

    if token_db is None:
        return True

    await delete_commit(session, token_db)

    return True


@router.get("/me", response_model=UserRead)
async def me(user: Annotated[UserDB, Depends(get_current_user)]):
    return user


@router.get("/", response_model=list[UserRead])
async def get_all(*, session: Annotated[AsyncSession, Depends(get_session)]):
    return await select_all_list(session, UserDB)


@router.post("/", response_model=UserRead)
async def create(
    *, session: Annotated[AsyncSession, Depends(get_session)], user: UserCreate
):
    user_db = UserDB.from_orm(
        user, {"hashed_password": pwd_context.hash(user.password)}
    )

    return await add_commit_refresh(session, user_db)


@router.get("/{id}", response_model=UserRead)
async def get(*, session: Annotated[AsyncSession, Depends(get_session)], id: int):
    return await get_or_404(session, UserDB, id)


@router.patch("/{id}", response_model=UserRead)
async def update(
    *, session: Annotated[AsyncSession, Depends(get_session)], id: int, user: UserUpdate
):
    user_db = await get_or_404(session, UserDB, id)

    update_instance(user_db, user)

    return await add_commit_refresh(session, user_db)


@router.delete("/{id}")
async def delete(*, session: Annotated[AsyncSession, Depends(get_session)], id: int):
    user_db = await get_or_404(session, UserDB, id)

    await delete_commit(session, user_db)

    return True
