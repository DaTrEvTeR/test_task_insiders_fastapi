from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.check_permission import check_permission
from app.dependencies.get_db import get_db
from app.permissions.schemas import PermissionRead
from app.roles.schemas import RoleCreate, RoleRead
from app.roles.repository import roles_repository
from app.config.roles_permissions_enums import PermissionsEnum
from app.permissions.repository import permissions_repository

roles_router = APIRouter(prefix="/roles", tags=["Roles"])


@roles_router.post("/", response_model=RoleRead)
async def create_role(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db),
):
    check_permission([PermissionsEnum.MANAGE_ROLES])
    new_role = await roles_repository.create_role(role_data, db)
    return new_role


@roles_router.get("/", response_model=list[RoleRead])
async def get_roles(
    db: AsyncSession = Depends(get_db),
):
    check_permission([PermissionsEnum.MANAGE_ROLES])
    roles = await roles_repository.read_roles(db)
    return roles


@roles_router.delete("/{role_id}")
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
):
    check_permission([PermissionsEnum.MANAGE_ROLES])
    role = await roles_repository.read_role(RoleRead(role_id=role_id), db)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    await roles_repository.delete_role(role, db)
    return {"message": "Role deleted successfully"}


@roles_router.put("/{role_id}/assign_permissions")
async def assign_permissions(
    role_id: int,
    permissions_data: list[int],
    db: AsyncSession = Depends(get_db),
):
    check_permission([PermissionsEnum.MANAGE_ROLES])
    role = await roles_repository.read_role(RoleRead(role_id=role_id), db)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permissions = []
    for permission_id in permissions_data:
        permission = await permissions_repository.read_permission(PermissionRead(permission_id=permission_id), db)
        if permission:
            permissions.append(permission)

    updated_role = await roles_repository.assign_permissions(role, permissions, db)
    return {"message": f"Permissions assigned to {updated_role.name} role successfully"}


@roles_router.put("/{role_id}/unassign_permissions")
async def unassign_permissions(
    role_id: int,
    permissions_data: list[int],
    db: AsyncSession = Depends(get_db),
):
    check_permission([PermissionsEnum.MANAGE_ROLES])
    role = await roles_repository.read_role(RoleRead(role_id=role_id), db)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permissions = []
    for permission_id in permissions_data:
        permission = await permissions_repository.read_permission(PermissionRead(permission_id=permission_id), db)
        if permission:
            permissions.append(permission)

    updated_role = await roles_repository.unassign_permissions(role, permissions, db)
    return {"message": f"Permissions removed from {updated_role.name} role successfully"}
