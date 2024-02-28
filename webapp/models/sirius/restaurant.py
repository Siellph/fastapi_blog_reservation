from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.dish import Dish


class Restaurant(Base):
    __tablename__ = 'restaurant'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    menu: Mapped[List['Dish']] = relationship(
        'Dish',
        secondary=f'{DEFAULT_SCHEMA}.restaurant_dish',
        back_populates='restaurant_id',
    )
