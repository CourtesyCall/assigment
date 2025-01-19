from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models import Base

if TYPE_CHECKING:
    from ..users.user import User
    from ..comments.comment import Comment


class Blog(Base):

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    author: Mapped["User"] = relationship(back_populates="blogs")
    comments: Mapped[list["Comment"]] = relationship(back_populates="blog")

    # author = relationship("User", back_populates="blogs")
    # comments = relationship("Comment", back_populates="blog", cascade="all, delete")
    # likes = relationship("Like", back_populates="blog", cascade="all, delete")
