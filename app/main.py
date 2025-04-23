from fastapi import FastAPI
from app.api.routes import activity
from app.core.lifespan import lifespan


def create_app() -> FastAPI:
    app = FastAPI(
        title="Activity Feed API",
        version="0.0.0",
        description="Mini Social Platform feed built with FastAPI, Kafka, Redis, Postgres",
        lifespan=lifespan,
    )

    app.include_router(activity.router)
    return app


app = create_app()
