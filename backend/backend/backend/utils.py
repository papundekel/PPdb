from typing import Any, TypeVar

from fastapi import HTTPException
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

T = TypeVar("T", bound=SQLModel)


async def get_not_id(
    session: AsyncSession, ModelDB: type[T], column: Any, pk: Any, *options: Any
) -> T | None:
    query = select(ModelDB).where(column == pk)

    if options != ():
        query = query.options(*options)

    instance_db = (await session.exec(query)).first()
    return instance_db


async def select_all_list(session: AsyncSession, ModelDB: type[T]) -> list[T]:
    query = select(ModelDB)
    result = await session.exec(query)  # type: ignore
    return list(result)


async def get_or_404(session: AsyncSession, ModelDB: Any, pk: Any):
    instance_db = await session.get(ModelDB, pk)

    if instance_db is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Object not found.")

    return instance_db


def update_instance(instance_db: Any, instance: Any) -> None:
    data = instance.dict(exclude_unset=True)

    for key, value in data.items():
        setattr(instance_db, key, value)


async def add_commit_refresh(session: AsyncSession, instance_db: Any):
    session.add(instance_db)
    await session.commit()
    await session.refresh(instance_db)
    return instance_db


async def delete_commit(session: AsyncSession, instance_db: Any) -> None:
    await session.delete(instance_db)
    await session.commit()
