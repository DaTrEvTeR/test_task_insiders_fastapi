from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base_model import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class Book(Base):
    __tablename__ = "books"
    # model attrs
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    author: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    # relationships
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="books", lazy="selectin")
