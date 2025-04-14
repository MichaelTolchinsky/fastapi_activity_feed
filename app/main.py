from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import activity
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before the app starts
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # After the app shuts down
    # (You can clean up things here if needed)
    pass


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title="Activity Feed API",
        version="0.0.0",
        description="Mini LinkedIn feed built with FastAPI, Kafka, Redis, Postgres",
    )

    app.include_router(activity.router)
    return app


app = create_app()
