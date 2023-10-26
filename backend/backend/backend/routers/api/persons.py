from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.database import get_session
from backend.models.person import PersonDB
from backend.schemas.person import PersonCreate, PersonRead, PersonUpdate
from backend.utils import add_commit_refresh, get_or_404

router = APIRouter(tags=["persons"], prefix="/persons")


@router.get("/", response_model=list[PersonRead])
async def __get_persons(*, session: AsyncSession = Depends(get_session)):
    query = select(PersonDB)
    result = await session.exec(query)  # type: ignore
    persons = list(result)
    return persons


@router.post("/", response_model=PersonRead)
async def __create_person(
    *, session: AsyncSession = Depends(get_session), person: PersonCreate
):
    person_db = PersonDB.from_orm(person)

    return await add_commit_refresh(session, person_db)


@router.get("/{id}/", response_model=PersonRead)
async def __get_person(*, session: AsyncSession = Depends(get_session), id: int):
    return await get_or_404(session, PersonDB, id)


@router.patch("/{id}/", response_model=PersonRead)
async def __update_person(
    *, session: AsyncSession = Depends(get_session), id: int, person: PersonUpdate
):
    person_db = await get_or_404(session, PersonDB, id)

    person_data = person.dict(exclude_unset=True)
    for key, value in person_data.items():
        setattr(person_db, key, value)

    return await add_commit_refresh(session, person_db)


@router.delete("/{id}/")
async def __delete_person(*, session: AsyncSession = Depends(get_session), id: int):
    person_db = await get_or_404(session, PersonDB, id)

    await session.delete(person_db)
    await session.commit()

    return True
