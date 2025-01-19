from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models import Base


if TYPE_CHECKING:
    from db.models.likes.category import Category
    from db.models.users.user import User


class Like(Base):

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    target_id: Mapped[int] = mapped_column(nullable=False)  # id of blog or comment
    user: Mapped["User"] = relationship(backref="likes")
    category: Mapped["Category"] = relationship(back_populates="likes")

    # post: Mapped["Blog"] = relationship(
    #     primaryjoin="and_(Like.category_id == Category.id, Category.name == 'post')",
    #     viewonly=True,
    # )
    # comment: Mapped["Comment"] = relationship(
    #     primaryjoin="and_(Like.category_id == Category.id, Category.name == 'comment')",
    #     viewonly=True,
    # )
