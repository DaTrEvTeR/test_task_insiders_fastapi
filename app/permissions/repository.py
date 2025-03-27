from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Permission
from app.permissions.schemas import PermissionCreate, PermissionRead


class PermissionsRepository:
    async def create_permission(self, model: PermissionCreate, db: AsyncSession) -> Permission:
        permission = Permission(name=model.name)
        db.add(permission)
        await db.commit()
        await db.refresh(permission)
        return permission

    async def read_permission(self, model: PermissionRead, db: AsyncSession) -> Permission | None:
        statement = select(Permission)
        if model.permission_id:
            statement = statement.filter_by(id=model.permission_id)
        if model.name:
            statement = statement.filter_by(name=model.name.lower())
        result = await db.execute(statement)
        return result.unique().scalar_one_or_none()

    async def read_permissions(self, db: AsyncSession) -> list[Permission]:
        statement = select(Permission)
        result = await db.execute(statement)
        permissions = result.unique().scalars().all()
        return list(permissions)

    async def remove_permission(self, permission: Permission, db: AsyncSession) -> None:
        await db.delete(permission)
        await db.commit()

    async def update_permission_title(self, permission: Permission, name: str, db: AsyncSession) -> Permission:
        permission.name = name
        db.add(permission)
        await db.commit()
        await db.refresh(permission)
        return permission


permissions_repository: PermissionsRepository = PermissionsRepository()
