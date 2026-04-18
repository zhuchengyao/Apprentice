import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session


async def execute_parallel(*stmts):
    """Run independent SELECT statements in parallel on separate sessions.

    AsyncSession forbids concurrent statements, so we open a fresh session
    per query. Returns Result objects in the same order as the inputs.
    """
    async def _run(stmt):
        async with async_session() as s:
            return await s.execute(stmt)
    return await asyncio.gather(*(_run(s) for s in stmts))
