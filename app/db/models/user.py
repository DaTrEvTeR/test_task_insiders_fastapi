from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import EmailType, PasswordType

from app.db.models.base_model import Base

if TYPE_CHECKING:
    from app.db.models.role import Role
    from app.db.models.book import Book


class User(Base):
    __tablename__ = "users"
    # table args
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(30), index=False, nullable=False)
    email: Mapped[EmailType] = mapped_column(EmailType(), index=True, nullable=False)
    password: Mapped[PasswordType] = mapped_column(PasswordType(schemes=["bcrypt"]), nullable=False)
    # relationships
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="selectin")
    books: Mapped[list["Book"]] = relationship(back_populates="user", lazy="selectin")
