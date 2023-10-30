from turtle import up
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.database import get_session
from backend.users.models import UserDB
from backend.users.schemas import UserCreate, UserRead, UserUpdate
from backend.utils import (
    add_commit_refresh,
    delete_commit,
    get_or_404,
    select_all_list,
    update_instance,
)

router = APIRouter(tags=["users"], prefix="/user")


@router.get("/", response_model=list[UserRead])
async def get_all(*, session: Annotated[AsyncSession, Depends(get_session)]):
    return await select_all_list(session, UserDB)


@router.post("/", response_model=UserRead)
async def create(
    *, session: Annotated[AsyncSession, Depends(get_session)], user: UserCreate
):
    user_db = UserDB.from_orm(user)

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


@router.get("login")
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return "login"
