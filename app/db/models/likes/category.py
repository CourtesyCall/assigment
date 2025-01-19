from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from db.models import Base


if TYPE_CHECKING:
    from ..likes.like import Like


class Category(Base):

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    model_path: Mapped[str] = mapped_column(nullable=False)
    likes: Mapped[list["Like"]] = relationship(back_populates="category")
