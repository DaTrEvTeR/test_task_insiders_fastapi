from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.check_permission import check_permission
from app.dependencies.get_db import get_db
from app.permissions.schemas import PermissionCreate, PermissionRead
from app.permissions.repository import permissions_repository
from app.config.roles_permissions_enums import PermissionsEnum

permissions_router = APIRouter(prefix="/permissions", tags=["Permissions"])


@permissions_router.post("/", response_model=PermissionRead)
async def create_permission(
    permission_data: PermissionCreate,
    db: AsyncSession = Depends(get_db),
):
    check_permission([PermissionsEnum.MANAGE_PERMISSIONS])
    new_permission = await permissions_repository.create_permission(permission_data, db)
    return new_permission


@permissions_router.get("/", response_model=list[PermissionRead])
async def get_permissions(
    db: AsyncSession = Depends(get_db),
):
    check_permission([PermissionsEnum.MANAGE_PERMISSIONS])
    permissions = await permissions_repository.read_permissions(db)
    return permissions


@permissions_router.delete("/{permission_id}")
async def delete_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_db),
):
    check_permission([PermissionsEnum.MANAGE_PERMISSIONS])
    permission = await permissions_repository.read_permission(PermissionRead(permission_id=permission_id), db)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    await permissions_repository.remove_permission(permission, db)
    return {"message": "Permission deleted successfully"}
