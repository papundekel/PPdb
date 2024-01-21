from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.database import get_session
from backend.persons.models import PersonDB
from backend.persons.schemas import PersonCreate, PersonRead, PersonUpdate
from backend.users.dependencies import require_login
from backend.utils import (
    add_commit_refresh,
    delete_commit,
    get_or_404,
    select_all_list,
    update_instance,
)

router = APIRouter(
    tags=["persons"], prefix="/persons", dependencies=[Depends(require_login)]
)


@router.get("/", response_model=list[PersonRead])
async def get_all(
    session: Annotated[AsyncSession, Depends(get_session)],
):
    return await select_all_list(session, PersonDB)


@router.post("/", response_model=PersonRead)
async def create(
    session: Annotated[AsyncSession, Depends(get_session)],
    person: PersonCreate,
):
    person_db = PersonDB.model_validate(person)

    return await add_commit_refresh(session, person_db)


@router.get("/{id}", response_model=PersonRead)
async def get(
    session: Annotated[AsyncSession, Depends(get_session)],
    id: int,
):
    return await get_or_404(session, PersonDB, id)


@router.patch("/{id}", response_model=PersonRead)
async def update(
    session: Annotated[AsyncSession, Depends(get_session)],
    id: int,
    person: PersonUpdate,
):
    person_db = await get_or_404(session, PersonDB, id)

    update_instance(person_db, person)

    return await add_commit_refresh(session, person_db)


@router.delete("/{id}")
async def delete(
    session: Annotated[AsyncSession, Depends(get_session)],
    id: int,
):
    person_db = await get_or_404(session, PersonDB, id)

    await delete_commit(session, person_db)

    return True
