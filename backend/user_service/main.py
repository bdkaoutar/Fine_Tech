from contextlib import asynccontextmanager

from fastapi import FastAPI

from user.routes import router
from database.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown logic (if needed) goes here


app = FastAPI(lifespan=lifespan)

app.include_router(router)
