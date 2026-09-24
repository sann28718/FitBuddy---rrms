from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup/shutdown lifecycle.
    """

    init_db()

    yield


app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description=(
        "AI-powered personalized workout and nutrition "
        "planning application."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
