from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models import Base


if TYPE_CHECKING:
    from ..blogs.blog import Blog
    from ..comments.comment import Comment


class User(Base):

    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    blogs: Mapped[list["Blog"]] = relationship(back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")

    __table_args__ = {"extend_existing": True}

    # blogs = relationship("Blog", back_populates="author", cascade="all, delete")
    # comments = relationship("Comment", back_populates="author", cascade="all, delete")
    # likes = relationship("Like", back_populates="user", cascade="all, delete")
