from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.kafka import close_kafka_producer, get_kafka_producer
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before the app starts
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await get_kafka_producer()

    yield

    # After the app shuts down
    await close_kafka_producer()
    pass
