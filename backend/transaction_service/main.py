from contextlib import asynccontextmanager
from fastapi import FastAPI
from transaction.routes import router
from database.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):  # Renommer 'app' en 'application'
    await init_db()
    yield

    # Shutdown logic (if needed) goes here


app = FastAPI(lifespan=lifespan)

app.include_router(router)