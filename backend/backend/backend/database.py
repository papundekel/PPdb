from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.settings import url

engine = create_async_engine(url, echo=True, connect_args={"check_same_thread": False})


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
