from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.database import get_session
from backend.users.dependencies import require_login
from backend.users.models import RegistrationApproval, RegistrationApprovalDB
from backend.utils import (
    add_commit_refresh,
    delete_commit,
    get_not_id,
    get_or_404,
    select_all_list,
)

router = APIRouter(
    prefix="/registration-approval",
    dependencies=[Depends(require_login)],
)


@router.get("/", response_model=list[RegistrationApproval])
async def get_all(
    session: Annotated[AsyncSession, Depends(get_session)],
):
    return await select_all_list(session, RegistrationApprovalDB)


@router.post("/", response_model=RegistrationApproval)
async def create(
    session: Annotated[AsyncSession, Depends(get_session)],
    approval: RegistrationApproval,
):
    approval_db = await get_not_id(
        session, RegistrationApprovalDB, RegistrationApprovalDB.email, approval.email
    )

    if approval_db is not None:
        return approval_db

    approval_db = RegistrationApprovalDB.model_validate(approval)

    return await add_commit_refresh(session, approval_db)


@router.delete("/{id}")
async def delete(
    session: Annotated[AsyncSession, Depends(get_session)],
    id: int,
):
    user_db = await get_or_404(session, RegistrationApprovalDB, id)

    await delete_commit(session, user_db)

    return True
