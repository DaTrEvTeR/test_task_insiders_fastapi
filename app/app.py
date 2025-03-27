from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from fastapi import FastAPI

from sqlalchemy.ext.asyncio import close_all_sessions

from app.db.config import engine  # noqa
from app.db import models  # noqa
from app.users.routes import auth_router
from app.utils.init_roles import init_roles


@asynccontextmanager
async def lifespan(initialized_app: FastAPI) -> AsyncGenerator[None, Any]:  # noqa  # type: ignore
    await init_roles()
    yield

    await close_all_sessions()
    await engine.dispose()


app = FastAPI(title="Library API", lifespan=lifespan)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Library API"}
