from fastapi import FastAPI
from app.db.config import engine  # noqa
from app.db.base_model import Base  # noqa

app = FastAPI(title="Library API")


@app.get("/")
async def root():
    return {"message": "Welcome to Library API"}
