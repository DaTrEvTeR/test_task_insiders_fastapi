from typing import TYPE_CHECKING
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.roles import RolesEnum
from app.db.models import User
from app.roles.schemas import RoleRead
from app.users.schemas import UserCreate, UserUpdate, UserSearch
from app.roles.repository import roles_repository

if TYPE_CHECKING:
    from app.db.models import Role


class UsersRepository:
    async def create_user(self, model: UserCreate, db: AsyncSession) -> User:
        role = None
        if model.role_id:
            res = await roles_repository.read_role(RoleRead(role_id=model.role_id), db)
            if res:
                role = res
        if not role:
            role = await roles_repository.read_role(RoleRead(name=RolesEnum.READER.value), db)
        user = User(
            email=model.email.lower(),
            username=model.username,
            password=model.password,
            role_id=role.id if role else None,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def read_user(self, model: UserSearch, db: AsyncSession) -> User | None:
        statement = select(User)
        if model.email:
            statement = statement.filter_by(email=model.email.lower())
        if model.username:
            statement = statement.filter_by(username=model.username.lower())
        if model.user_id:
            statement = statement.filter_by(username=model.user_id)
        result = await db.execute(statement)
        return result.unique().scalar_one_or_none()

    async def read_users(self, db: AsyncSession) -> list[User]:
        statement = select(User)
        result = await db.execute(statement)
        users = result.unique().scalars().all()
        return list(users)

    async def read_users_with_filters(self, model: UserSearch, db: AsyncSession) -> list[User]:
        statement = select(User).where(
            or_(User.id == model.user_id, User.username == model.username, User.email == model.email)
        )
        result = await db.execute(statement)
        users = result.unique().scalars().all()
        return list(users)

    async def update_user(self, user: User, new_data: UserUpdate, db: AsyncSession) -> User:
        if new_data.email:
            user.email = new_data.email.lower()
        if new_data.password:
            user.password = new_data.password
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def assign_role(self, user: User, role: "Role", db: AsyncSession) -> User:
        user.role = role
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def delete_user(self, user: User, db: AsyncSession) -> None:
        await db.delete(user)
        await db.commit()


users_repository: UsersRepository = UsersRepository()
