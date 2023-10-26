from typing import Any

from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_or_404(session: AsyncSession, ModelDB: Any, pk: Any):
    instance_db = await session.get(ModelDB, pk)

    if instance_db is None:
        raise HTTPException(status_code=404, detail="Object not found")

    return instance_db


async def add_commit_refresh(session: AsyncSession, instance_db: Any):
    session.add(instance_db)
    await session.commit()
    await session.refresh(instance_db)
    return instance_db
