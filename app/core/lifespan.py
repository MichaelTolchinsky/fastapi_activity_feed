from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    pass
