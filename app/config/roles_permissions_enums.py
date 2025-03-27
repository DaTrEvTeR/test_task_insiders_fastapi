import enum


class RolesEnum(enum.StrEnum):
    READER = "reader"
    WRITER = "writer"
    ADMIN = "admin"


class PermissionsEnum(enum.StrEnum):
    WRITE = "write"
    READ = "read"
    UPDT_OWN = "update_own"
    DLT_OWN = "delete_own"
    UPDT_ANY = "update_any"
    DLT_ANY = "delete_any"
    MANAGE_PERMISSIONS = "manage_permissions"
    MANAGE_ROLES = "manage_roles"


roles_permission_map = {
    RolesEnum.READER: [PermissionsEnum.READ],
    RolesEnum.WRITER: [
        PermissionsEnum.READ,
        PermissionsEnum.WRITE,
        PermissionsEnum.UPDT_OWN,
        PermissionsEnum.DLT_OWN,
    ],
    RolesEnum.ADMIN: [
        PermissionsEnum.READ,
        PermissionsEnum.WRITE,
        PermissionsEnum.UPDT_ANY,
        PermissionsEnum.DLT_ANY,
        PermissionsEnum.MANAGE_PERMISSIONS,
    ],
}
