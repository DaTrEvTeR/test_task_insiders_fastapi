from typing import TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base_model import Base

if TYPE_CHECKING:
    from app.db.models.role import Role


class Permission(Base):
    __tablename__ = "permissions"
    # model attrs
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    # relationships
    roles: Mapped[list["Role"]] = relationship(
        secondary="roles_permissions", back_populates="permissions", lazy="selectin"
    )
