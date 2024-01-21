from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_403_FORBIDDEN

from backend.database import get_session
from backend.users import oauth2_scheme, pwd_context
from backend.users.dependencies import require_login
from backend.users.models import AccessToken, RegistrationApprovalDB, TokenDB, UserDB
from backend.users.routers.api import registration_approval
from backend.users.schemas import UserCreate, UserRead, UserUpdate
from backend.utils import (
    add_commit_refresh,
    delete_commit,
    get_not_id,
    get_or_404,
    select_all_list,
    update_instance,
)

router = APIRouter(tags=["users"], prefix="/users")


def make_acess_token(token_db: TokenDB):
    return AccessToken(access_token=token_db.token, token_type="bearer")


@router.post("/login", response_model=AccessToken)
async def login(
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    if token is not None:
        token_db = await get_not_id(session, TokenDB, TokenDB.token, token)

        if token_db is not None:
            return make_acess_token(token_db)

    email = form.username
    password = form.password

    user_db = await get_not_id(session, UserDB, UserDB.email, email)

    exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Incorrect email or password."
    )

    if user_db is None:
        raise exception

    password_matches = pwd_context.verify(password, user_db.hashed_password)

    if not password_matches:
        raise exception

    token_db = TokenDB(
        token=token_urlsafe(),
        expires=datetime.now() + timedelta(days=2),
        user=user_db,
    )  # type: ignore

    await add_commit_refresh(session, token_db)

    return make_acess_token(token_db)


@router.delete("/login")
async def logout(
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    if token is None:
        return True

    token_db = (
        await session.exec(select(TokenDB).where(TokenDB.token == token))
    ).first()

    if token_db is None:
        return True

    await delete_commit(session, token_db)

    return True


@router.get("/current", response_model=UserRead)
async def current(current_user: Annotated[UserDB, Depends(require_login)]):
    return current_user


crud_router = APIRouter()


@crud_router.get(
    "/", response_model=list[UserRead], dependencies=[Depends(require_login)]
)
async def get_all(
    session: Annotated[AsyncSession, Depends(get_session)],
):
    return await select_all_list(session, UserDB)


@crud_router.post("/", response_model=UserRead)
async def create(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: UserCreate,
):
    approval_db = await get_not_id(
        session,
        RegistrationApprovalDB,
        RegistrationApprovalDB.email,
        user.email,
    )

    if approval_db is None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="User registration not approved."
        )

    user_db = UserDB.model_validate(
        user, update={"hashed_password": pwd_context.hash(user.password)}
    )

    await session.delete(approval_db)
    return await add_commit_refresh(session, user_db)


@crud_router.get(
    "/{id}", response_model=UserRead, dependencies=[Depends(require_login)]
)
async def get(
    session: Annotated[AsyncSession, Depends(get_session)],
    id: int,
):
    return await get_or_404(session, UserDB, id)


@crud_router.patch(
    "/{id}", response_model=UserRead, dependencies=[Depends(require_login)]
)
async def update(
    session: Annotated[AsyncSession, Depends(get_session)],
    id: int,
    user: UserUpdate,
):
    user_db = await get_or_404(session, UserDB, id)

    update_instance(user_db, user)

    return await add_commit_refresh(session, user_db)


@crud_router.delete("/{id}", dependencies=[Depends(require_login)])
async def delete(
    session: Annotated[AsyncSession, Depends(get_session)],
    id: int,
):
    user_db = await get_or_404(session, UserDB, id)

    await delete_commit(session, user_db)

    return True


router.include_router(crud_router)
router.include_router(registration_approval.router)
