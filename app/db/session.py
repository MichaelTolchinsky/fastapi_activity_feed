from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import SessionLocal
from typing import AsyncGenerator


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
