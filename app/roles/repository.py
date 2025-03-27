from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Permission, Role
from app.roles.schemas import RoleCreate, RoleRead


class RolesRepository:
    async def create_role(self, model: RoleCreate, db: AsyncSession) -> Role:
        role = Role(name=model.name.lower())
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role

    async def read_role(self, model: RoleRead, db: AsyncSession) -> Role | None:
        statement = select(Role)
        if model.role_id:
            statement = statement.filter_by(id=model.role_id)
        if model.name:
            statement = statement.filter_by(name=model.role_name.lower())
        result = await db.execute(statement)
        return result.unique().scalar_one_or_none()

    async def read_roles(self, db: AsyncSession) -> list[Role]:
        statement = select(Role)
        result = await db.execute(statement)
        roles = result.unique().scalars().all()
        return list(roles)

    async def delete_role(self, role: Role, db: AsyncSession) -> None:
        await db.delete(role)
        await db.commit()

    async def assign_permissions(self, role: Role, permissions: list[Permission], db: AsyncSession) -> Role:
        for permission in permissions:
            if permission not in role.permissions:
                role.permissions.append(permission)
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role

    async def unassign_permissions(self, role: Role, permissions: list[Permission], db: AsyncSession) -> Role:
        for permission in permissions:
            if permission in role.permissions:
                role.permissions.remove(permission)
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role

    async def update_role_name(self, role: Role, name: str, db: AsyncSession) -> Role:
        role.name = name
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role


roles_repository: RolesRepository = RolesRepository()
