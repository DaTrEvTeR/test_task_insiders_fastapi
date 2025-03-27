from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base_model import Base


class RolePermission(Base):
    __tablename__ = "roles_permissions"
    __table_args__ = (PrimaryKeyConstraint("role_id", "permission_id"),)
    # relationships
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)
