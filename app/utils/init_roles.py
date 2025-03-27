from sqlalchemy.future import select
from app.db.config import session_maker
from app.db.models import Role, Permission
from app.config.roles_permissions_enums import RolesEnum, PermissionsEnum, roles_permission_map
from app.roles.repository import roles_repository
from app.permissions.repository import permissions_repository
from app.roles.schemas import RoleCreate
from app.permissions.schemas import PermissionCreate


async def init_roles():
    async with session_maker() as db:
        stm = select(Role)
        res = await db.execute(stm)
        roles_in_db = res.unique().scalars().all()
        roles_names_map = {role.name: role for role in roles_in_db}
        for role in RolesEnum:
            if role.value not in roles_names_map:
                roles_names_map[role.value] = await roles_repository.create_role(RoleCreate(name=role.value), db)

        permissions_in_db = (await db.execute(select(Permission))).unique().scalars().all()
        permissions_names_map = {permission.name: permission for permission in permissions_in_db}
        for permission in PermissionsEnum:
            if permission.value not in permissions_names_map:
                permissions_names_map[permission.value] = await permissions_repository.create_permission(
                    PermissionCreate(name=permission.value), db
                )

        for r, p in roles_permission_map.items():
            role = roles_names_map[r]
            for prmsn in p:
                if permissions_names_map[prmsn.value] not in role.permissions:
                    role.permissions.append(permissions_names_map[prmsn.value])
            db.add(role)
            await db.commit()
