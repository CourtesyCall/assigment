from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models import Base


if TYPE_CHECKING:
    from db.models.blogs.blog import Blog
    from db.models.users.user import User


class Comment(Base):

    content: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    blog_id: Mapped[int] = mapped_column(ForeignKey("blogs.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # author = relationship("User", back_populates="comments")
    # blog = relationship("Blog", back_populates="comments")

    blog: Mapped["Blog"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")
