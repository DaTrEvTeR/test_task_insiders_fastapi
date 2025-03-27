from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from app.db.models.base_model import Base

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.permision import Permission


class Role(Base):
    __tablename__ = "roles"
    # model attrs
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    # relationships
    users: Mapped[list["User"]] = relationship(back_populates="role", lazy="selectin")
    permissions: Mapped[list["Permission"]] = relationship(
        secondary="roles_permissions", back_populates="roles", lazy="selectin"
    )
