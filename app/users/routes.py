from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User
from app.db.get_db import get_db
from app.users.jwt import create_access_token
from app.users.schemas import UserCreate, UserLogin, TokenData, UserSearch
from app.users.repository import users_repository

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=TokenData)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    if await users_repository.read_user(UserSearch(email=user_data.email), db):
        raise HTTPException(status_code=400, detail="User with this email is already registered")
    if await users_repository.read_user(UserSearch(username=user_data.username), db):
        raise HTTPException(status_code=400, detail="User with this username is already registered")

    new_user = await users_repository.create_user(user_data, db)

    token = create_access_token(data={"sub": new_user.email})
    return TokenData(access_token=token, token_type="bearer")


@auth_router.post("/login", response_model=TokenData)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).filter(User.username == user_data.username))
    user = user.scalars().first()

    if not user or not user_data.password == user.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_access_token(data={"sub": user.email})
    return TokenData(access_token=token, token_type="bearer")
