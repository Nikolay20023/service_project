from typing import AsyncGenerator
from core.config import app_setting
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


engine = create_async_engine(
    app_setting.database_dsn.unicode_string(), echo=True, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
