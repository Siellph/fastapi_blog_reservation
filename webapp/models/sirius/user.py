from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.file import File


class User(Base):
    __tablename__ = 'user'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    username: Mapped[str] = mapped_column(String, unique=True)

    hashed_password: Mapped[str] = mapped_column(String)

    files: Mapped[List['File']] = relationship(
        'File',
        secondary=f'{DEFAULT_SCHEMA}.user_file',
        back_populates='users',
    )
